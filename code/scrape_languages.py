import json
import requests
import os
import time

with open('../data/auth_data.txt', 'rt') as conn:
    auth_data = conn.read()

user = auth_data[0]
pword = auth_data[1]

user_jsons = os.listdir('../data/')
user_jsons = [j for j in user_jsons if 'json' in j]

# Store the language urls for each user in a list,
# one entry per user
language_urls = []
for j in user_jsons:
    with open(j, 'rt') as conn:
        user_repos = json.load(conn)
    l_urls = [repo['language_url'] for repo in user_repos]
    language_urls.append(l_urls)



# Scrape the urls per user and return the languages
throttle_period = 0.7 # 5k requests/hour = 1.3 requests / s, so wait 0.7s btwn requests
bytes_threshold = 100
user_langs = []
for user in language_urls:
    temp = {}
    for repo_url in user:
        repo_langs = requests.get(repo_url,
                                  auth=(user,
                                        pword
                                        )
                                  )
        langs = repo_langs.json()
        for l in langs:
            if langs[l] > bytes_threshold:
                if l in temp:
                    temp[l] += 1
                else:
                    temp[l] = 1
    time.sleep(throttle_period)
    user_langs.append(temp)
                

    
