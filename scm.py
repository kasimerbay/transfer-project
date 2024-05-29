"""
This library is created to transfer projects across Bankalararası Kart Merkezi 's SCM tools.

By Ahmet Kasım Erbay: 20.02.2024 - 16:17:25
"""

import subprocess,os


class Instance:
    def __init__(self, instance, user):
        self.instance = instance
        self.user = user

    def api_to_json(self, api_call):
        words = {"true":"True", "false":"False"}

        for key,value in words.items():
            api_call = api_call.replace(key, value)

        try:
            api_call = eval(api_call)
        except:
            raise Exception(f"Please be sure {self.user[:self.user.index(':')]} has right permissions in {self.key} on {self.instance}")

        return api_call

    def list_projects(self):

        command = f"curl -k -u{self.user} https://{self.instance}/rest/api/1.0/projects?limit=100"

        api_call = self.run(command)
        api_call = self.api_to_json(api_call)

        return [api_call["values"][i]["key"] for i in range(int(api_call["size"]))]

    def run(self, command):
        # print(command)
        return subprocess.run(command.split(" "), cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")

    def run_post(self, command):
        stream = os.popen(command)
        output = stream.read().strip()

        return output


class Project(Instance):

    def __init__(self, instance, user, key):
        self.key = key
        super().__init__(instance, user)

    def list_repositories(self):
        command = f"curl -k -u{self.user} https://{self.instance}/rest/api/1.0/projects/{self.key}/repos?limit=100"

        api_call = self.run(command)
        api_call = self.api_to_json(api_call)

        return [api_call["values"][i]["name"] for i in range(int(api_call["size"]))]

    def mirror_repos(self, repo_list, target_scm):

        repository_list = self.list_repositories()

        error_list = []

        for repo_name in repo_list:
            if repo_name in repository_list:
                try:
                    repo = Repository(self.instance, self.user, self.key, repo_name)
                    repo.clone()
                    repo.push(target_scm=target_scm)
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

        repository_list = self.list_repositories()

        return self.mirror_repos(repo_list=repository_list, target_scm=target_scm)


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

    def create_repository(self, target_scm):

        DICT = dict()

        PROJECT = """{"key":"%s","avatarUrl":"","avatar":"","links":%s}"""%(self.key,DICT)

        DATA = """{"name":"%s","project":%s,"slug":"%s","scmId":"git","links":%s}"""%(self.repo_name,PROJECT,self.repo_name,DICT)

        command = f"curl -u '{self.user}' --request POST --url 'https://{target_scm}/rest/api/latest/projects/{self.key}/repos' --header 'Accept:application/json' --header 'Content-Type:application/json' --data '{DATA}'"

        try:
            self.run_post(command)
        except:
            raise Exception(f"There is a problem occured in creation of {self.repo_name} on {target_scm}.")