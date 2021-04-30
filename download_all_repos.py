import pandas as pd
import os
import requests
import argparse
from m01_init_build import DEFAULT_GROUPS_FILE

# Token used to access all github repositories
GITHUB_ACCESS_TOKEN_FILE = 'github_access_token.txt'

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download repositories of ing-sw")

    parser.add_argument("-d", "--debug", action='store_true',
                        help="If present, print debug messages")
    parser.add_argument("-i", "--groups_file", default=DEFAULT_GROUPS_FILE,
                        help="Path to the CSV containing the groups")
    args = parser.parse_args()
    debug = args.debug
    groups_file = args.groups_file

    with open(GITHUB_ACCESS_TOKEN_FILE, 'r') as f:
        gihub_access_token = f.readline().strip()
    print(f"read access token {gihub_access_token}")

    df = pd.read_csv(groups_file, header=None).dropna()

    # Create a directory for all projects;
    repository_dir = "repos"
    if not os.path.isdir(repository_dir):
        os.mkdir(repository_dir)

    for index, row in df.iterrows():

        group_id = 'group-%02d' % int(row[0])
        url_repo = str(row[1]).replace('https://github.com/', 'https://' + gihub_access_token + '@github.com/')

        print(group_id, url_repo)
        os.system(f"cd {repository_dir}; git clone {url_repo}")
   
