"""
This library is created to transfer projects across Bankalararası Kart Merkezi 's SCM tools.

By Ahmet Kasım Erbay: 20.02.2024 - 16:17:25
"""

import subprocess
from dels.bitbucket_json import repos

class Instance:
    def __init__(self, instance, user):
        self.instance = instance
        self.user = user

    def get_repos(self):
        return [repos["values"][i]["name"] for i in range(int(repos["size"]))]

    def run(self, command):
        print(command)
        subprocess.run(command.split(" "))

class Project(Instance):

    def __init__(self, instance, user, key):
        self.key = key
        super().__init__(instance, user)


    def mirror_repos(self, repo_list, target_scm):

        repository_list = self.get_repos()

        error_list = []

        for repo_name in repo_list:
            if repo_name in repository_list:
                try:
                    repo = Repository(self.instance, self.user, self.key, repo_name)
                    repo.clone()
                    repo.push(target_scm)
                except:
                    error_list.append(f"{repo_name} -- " + "Clone or Push Error!")
                    continue
            else:
                error_list.append(f"{repo_name} -- " + f"There is no {repo_name} in the remote {self.instance}. Please Check!")

        if len(error_list)!= 0:
            print("\n\n------ List of untransferred repositories:")
            for error_repo in error_list:
                print("* ", error_repo)
            print(f"Total: {len(error_list)}")


    def mirror(self, target_scm):

        repository_list = self.get_repos()

        return self.mirror_repos(repository_list, target_scm)


class Repository(Project):

    def __init__(self, instance, user, key, repo_name):
        self.repo_name = repo_name
        super().__init__(instance, user, key)


    def clone(self):

        clone_ = f"https://{self.user}@{self.instance}/scm/{self.key.upper()}/{self.repo_name}.git repos/{self.repo_name}"
        command = f"git clone --mirror {clone_}"

        self.run(command)

    def push(self, target_scm):

        push_ = f"https://{self.user}@{target_scm}/scm/{self.key.lower()}/{self.repo_name}.git"
        command = f"git -C repos/{self.repo_name} push {push_} --all"

        self.run(command)
