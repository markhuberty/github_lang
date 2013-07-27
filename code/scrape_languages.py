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
 
            if id in user_language_urls:
                user_language_urls[repo_owner].append(l_url)
            else:
                user_language_urls[repo_owner] = [l_url]
            url_count += 1
            if url_count % 10000 == 0:
                print url_count



# Total repo count is very large.
# So shuffle by user and then retrieve up to N repos
k_urls = 100000
throttle_period = 0.7 # 5k requests/hour = 1.3 requests / s, so wait 0.7s btwn requests
bytes_threshold = 100


# Run through the shuffled list with a generator
def return_random_user(dict_input, N):
    k_vals = random.sample(dict_input.keys(), N)
    for k in k_vals:
        yield (k, dict_input[k])

user_gen = return_random_user(user_language_urls, k_urls)

user_langs = {}
user_count = 0
for git_user, lang_urls in user_gen:

    user_count += 1
    if user_count % 10000 == 0:
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
    
                

    
