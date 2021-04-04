import pandas as pd
import os
import requests
import argparse

# Token used to access all github repositories
GITHUB_ACCESS_TOKEN_FILE = 'github_access_token.txt'
SONAR_URL = 'http://localhost:9000/api/projects/create'
DEFAULT_GROUPS_FILE = "groups/groups.csv"

BUILD_SCRIPT = '#! /bin/bash\n' \
             'log_folder="build_logs_$(date +%Y-%m-%d_%H-%M-%S)"\n' \
             'mkdir -p logs\n' \
             'mkdir -p logs/$log_folder\n'

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download and test repositories of ing-sw")

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

    for index, row in df.iterrows():

        group_id = 'group-%02d' % int(row[0])
        url_repo = str(row[1]).replace('https://github.com/', 'https://' + gihub_access_token + '@github.com/')
        dir_name = os.path.basename(url_repo)

        print(group_id, url_repo, dir_name)

        # CREATE SONAR PROJECTS
        params = {'key': group_id, 'name': group_id}
        requests.post(SONAR_URL, params=params)

        # ADD PROJECT TO BUILDFILE
        BUILD_SCRIPT += 'sudo docker build . -t "ingsw"'
        BUILD_SCRIPT += ' --network=host --build-arg CACHE_DATE=$(date +%Y-%m-%d_%H-%M-%S)'
        BUILD_SCRIPT += ' --build-arg GROUP_ID="' + group_id + '"'
        BUILD_SCRIPT += ' --build-arg GROUP_REPO="' + url_repo + '"'
        BUILD_SCRIPT += ' --build-arg GROUP_DIR="' + dir_name + '"'
        BUILD_SCRIPT += '  | tee logs/$log_folder/' + group_id + '_RAW.txt\n'
        
    with open('m02_build.sh', 'w') as f:
        f.write(BUILD_SCRIPT)
    os.system("chmod +x m02_build.sh")