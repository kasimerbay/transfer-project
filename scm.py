"""
This library is created to transfer projects across Bankalararası Kart Merkezi 's SCM tools.

By Ahmet Kasım Erbay: 20.02.2024 - 16:17:25
"""

import os, json

class Instance:
    def __init__(self, instance, user):
        self.instance = instance
        self.user = user

    def get_projects(self):
        projects = self.api_to_json(self.run(f"curl -k -u{self.user} https://{self.instance}:/rest/api/1.0/projects/?limit=100"))

        print([projects["values"][i]["key"] for i in range(int(projects["size"]))])

    @staticmethod
    def api_to_json(api_call):

        to_replace = {"true":"True", "false":"False"}

        output = api_call.read()

        for key, value in to_replace.items():
            output.replace(key, value)

        try:
            return json.loads(output)

        except:
            raise Exception("Could not convert stream to json... Try to update your API object")


    def run(self, command):

        command = os.popen(command)

        return command

class Project(Instance):

    def __init__(self, instance, user, key):
        self.key = key
        super().__init__(instance, user)

    def project_info(self):
        stream = self.run(f"curl -k -u{self.user} https://{self.instance}/rest/api/1.0/projects/{self.key}/repos?limit=100")
        api_call = self.api_to_json(stream)

        repository_list = [api_call["values"][i]["name"] for i in range(int(api_call["size"]))]
        size = api_call["size"]
        is_last_page = api_call["isLastPage"]

        return repository_list, size, is_last_page

    def mirror_repos(self, repo_list, target_scm):

        repository_list, _, _ = self.project_info()
        error_list = []

        for repo_name in repo_list:
            if repo_name in repository_list:
                try:
                    repo = Repository(self.instance, self.user, self.key, repo_name)
                    repo.clone()
                    repo.push(target_scm)
                except:
                    error_list.append(f"{repo_name} -- " + "Clone Error!")
                    continue
            else:
                error_list.append(f"{repo_name} -- " + f"There is no {repo_name} in the remote {self.instance}. Please Check!")

        if len(error_list)!= 0:
            print("\n\n------ List of untransferred repositories:")
            for error_repo in error_list:
                print("* ", error_repo)
            print(f"Total: {len(error_list)}")


    def mirror(self, target_scm):

        repository_list, _, _ = self.project_info()

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
