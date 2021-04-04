import pandas as pd
import os
import requests


# Token used to access all github repositories
github_access_token = '1a64a9d30164eac48c5b365029a7fe93ef0cc296'
df = pd.read_csv("groups.csv", header=None).dropna()

# Create a directory for all projects;
repository_dir = "repos"
if not os.path.isdir(repository_dir):
    os.mkdir(repository_dir)

for index, row in df.iterrows():

    group_id = 'group-%02d' % int(row[0])
    url_repo = str(row[1]).replace('https://github.com/', 'https://' + github_access_token + '@github.com/')

    print(group_id, url_repo)
    os.system(f"cd {repository_dir}; git clone {url_repo}")
   
