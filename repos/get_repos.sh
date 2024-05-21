#!/bin/bash

echo -n "repos=" > bitbucket_json.py
curl -k -u infosec:BKMinfosec123 https://bitbucket.bkm.com.tr/rest/api/1.0/projects/SWC/repos?limit=100 >> bitbucket_json.py
sed -i 's/true/True/g' bitbucket_json.py
sed -i 's/false/False/g' bitbucket_json.py

echo "Json File is ready to repositonize"

python3 get_repos.py