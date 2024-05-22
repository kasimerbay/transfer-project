"""
Project Atlas

This project is created for project transfer accross SCM Tool instances.
"""

from module import *
import sys
from dels.bitbucket_json import repos

def main():

    user = sys.argv[1]
    key = sys.argv[2]
    source_scm = sys.argv[3]
    target_scm = sys.argv[4]

    repo_names = get_repos(repos)

    clone_repos(source_scm, key, repo_names, user)

    push_repos(target_scm, key, repo_names, user)

    delete_files()

if __name__ == "__main__":
    main()
