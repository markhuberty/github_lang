import json
import requests
import os
import time
import random

with open('../data/auth_data.txt', 'rt') as conn:
    auth_data = conn.read().splitlines()

user = auth_data[0]
pword = auth_data[1]

json_dir = '/home/markhuberty/github_data/'
repo_jsons = os.listdir(json_dir)
repo_jsons = [j for j in repo_jsons if 'json' in j]

# Store the language urls for each user in a list,
# one entry per user
url_count = 0
user_language_urls = {}

for j in repo_jsons:
    with open(json_dir + j, 'rt') as conn:
        repos = json.load(conn)
    for repo in repos:
        if not repo['fork']:

            try:
                repo_owner = repo['owner']['id']
            except:
                continue
            
            l_url = repo['languages_url']
 
            if repo_owner in user_language_urls:
                user_language_urls[repo_owner].append(l_url)
            else:
                user_language_urls[repo_owner] = [l_url]
            url_count += 1
            if url_count % 10000 == 0:
                print url_count



# Total repo count is very large.
# So shuffle by user and then retrieve up to N repos
k_users = 200000
throttle_period = 0.7 # 5k requests/hour = 1.3 requests / s, so wait 0.7s btwn requests
bytes_threshold = 100


# Run through the shuffled list with a generator
def return_random_user(k_vals, dict_input):
    k_vals = random.sample(dict_input.keys(), N)
    for k in k_vals:
        yield (k, dict_input[k])

# user_gen = return_random_user(user_language_urls, 300000)

user_langs = {}
user_count = 0
users = user_language_urls.keys()
random.shuffle(users)

for git_user in users:
    lang_urls = user_language_urls[git_user]
    if user_count > k_users:
        break
    if len(lang_urls) < 5:
        continue

    if user_count % 100 == 0:
        print user_count
        
    temp = {}
    for repo_url in lang_urls:
        repo_langs = requests.get(repo_url,
                                  auth=(user,
                                        pword
                                        )
                                  )

        try:
            repo_langs.raise_for_status()
        except requests.exceptions.HTTPError:
            print 'dead url'
            continue

        langs = repo_langs.json()
        for l in langs:
            if langs[l] > bytes_threshold:
                if l in temp:
                    temp[l] += 1
                else:
                    temp[l] = 1
        time.sleep(throttle_period)
    if len(temp) > 0:
        user_langs[git_user] = temp
        user_count += 1


import pandas as pd
all_langs = []
for v in user_langs.values():
    all_langs.extend(v)

lang_counts = pd.Series(all_langs).value_counts()
df_user_lang = pd.DataFrame(user_langs).transpose()
df_user_lang.fillna(0, inplace=True)

lang_counts.name = 'repo_ct'
lang_counts.to_csv('../data/github_lang_counts.csv', header=True, index_label='lang')

df_user_lang.to_csv('../data/github_user_lang_matrix.csv', index=False)

# Then convert to a binary 1/0 on whether user uses language
df_user_lang_binary = df_user_lang / df_user_lang
df_user_lang_binary.fillna(0, inplace=True)

user_lang_counts = df_user_lang_binary.sum(axis=0)

# Subset to only those langs w/ > 10 users:
user_lang_counts = user_lang_counts[user_lang_counts >= 10]

# And subset the matrix accordingly
df_user_lang_binary = df_user_lang_binary[user_lang_counts.index.values]

# Compute the co-occurrance rates
lang_cooc = df_user_lang_binary.T.dot(df_user_lang_binary)

# Divide out by the overall lang counts
lang_cooc = lang_cooc / user_lang_counts
lang_cooc.to_csv('../data/github_lang_cooc_matrix.csv', index=True)


p_ab = pd.DataFrame(np.triu(lang_cooc), index=lang_cooc.index, columns=lang_cooc.columns)
p_ba = pd.DataFrame(np.tril(lang_cooc), index=lang_cooc.index, columns=lang_cooc.columns)


def unpivot(frame):
    N, K = frame.shape
    data = {'value' : frame.values.ravel('F'),
            'lang_b' : np.tile(np.asarray(frame.index), K),
            'lang_a' : np.asarray(frame.columns).repeat(N)
            }
    df = pd.DataFrame(data)
    df.columns = ['lang_a', 'lang_b', 'p_ba']
    return df #pd.DataFrame(data, columns=['lang_a', 'lang_b', 'p'])


df_ab = unpivot(lang_cooc)
df_ab = df_ab[(df_ab.p_ba > 0) & (df_ab.p_ba < 1)]
df_ab.sort('p_ba', ascending=False, inplace=True)

df_ab.to_csv('../data/lang_cooc_edgelist.csv', index=False)
