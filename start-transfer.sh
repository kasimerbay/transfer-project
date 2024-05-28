#!/bin/bash

touch dels/bitbucket_json.py
echo -n 'repos=' > dels/bitbucket_json.py
curl -k -u $USER https://$SOURCE_SCM/rest/api/1.0/projects/$KEY/repos?limit=100 >> dels/bitbucket_json.py
sed -i 's/true/True/g' dels/bitbucket_json.py
sed -i 's/false/False/g' dels/bitbucket_json.py

python3 main.py $USER $KEY $SOURCE_SCM $TARGET_SCM