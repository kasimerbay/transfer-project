"""
This library is created to transfer projects across Bankalararası Kart Merkezi 's SCM tools.

By Ahmet Kasım Erbay: 20.02.2024 - 16:17:25
"""

from queue import Empty
import subprocess,os


class Instance:
    print("Welcome!, You'r privileged to work with the Atlassian Prince... Enjoy the show :)", end="\n\n")
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
            raise Exception(f"Please be sure {self.user[:self.user.index(':')]} has right permissions in {self.key} on {self.instance}.\nOr this means your api_call returned an empty string.")

        return api_call

    def list_projects(self):

        command = f"curl -k -u{self.user} https://{self.instance}/rest/api/1.0/projects?limit=100"

        api_call = self.run(command)
        api_call = self.api_to_json(api_call)

        return [api_call["values"][i]["key"] for i in range(int(api_call["size"]))]

    def run(self, command):
        print(command)
        return subprocess.run(command.split(" "), cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")

    def run_post(self, command):
        
        stream = os.popen(command)
        output = stream.read().strip()
        print(output)

        return output


class Project(Instance):

    def __init__(self, instance, user, key):
        self.key = key
        super().__init__(instance, user)

    def list_repositories(self):
        command = f"curl -k -u{self.user} https://{self.instance}/rest/api/1.0/projects/{self.key}/repos?limit=100"
        try:

            api_call = self.run(command)
            api_call = self.api_to_json(api_call)

            return [api_call["values"][i]["name"] for i in range(int(api_call["size"]))]
        except:
            return []

    def mirror_repos(self, repo_list, target_scm):

        target = Project(instance=target_scm, user=self.user, key=self.key)

        error_list = []
        # If target does not have the project, this for loop creates the project
        if target.key not in target.list_projects():
            target.create_project()

        repository_list = target.list_repositories()
        # If target has some missing repositories, this loop creates them
        for repo_name in repo_list:
            if repo_name not in repository_list:
                Repository(instance=target_scm, user=self.user, key=self.key, repo_name=repo_name).create_repository()

        for repo_name in repo_list:
            try:
                repo = Repository(self.instance, self.user, self.key, repo_name)
                repo.clone()
                repo.push(target_scm=target_scm)
            except:
                error_list.append(f"{repo_name} -- " + "Clone or Push Error!")
                continue

        if len(error_list)!= 0:
            print("\n\n------ List of untransferred repositories:")
            for error_repo in error_list:
                print("* ", error_repo)
            print(f"Total: {len(error_list)}")

    def mirror(self, target_scm):

        repository_list = self.list_repositories()

        return self.mirror_repos(repo_list=repository_list, target_scm=target_scm)

    def create_project(self):
        
        PROJECT_URL = f'https://{self.instance}/rest/api/latest/projects'
        DICT = dict()
        create_project = """curl --request POST -u %s --url '%s' --header 'Accept:application/json' --header 'Content-Type:application/json' --data '{"key":"%s","avatarUrl":"","avatar":"","links": %s}'"""%(self.user, PROJECT_URL, self.key ,DICT)

        try:
            self.run_post(create_project)
        except:
            raise Exception(f"Could not create {self.key} on {self.instance}.")


    def delete_project(self):

        PROJECT_DELETE_URL = f'https://{self.instance}/rest/api/latest/projects/{self.key}'
        delete_project = """curl --request DELETE -u '%s' --url '%s'"""%(self.user, PROJECT_DELETE_URL)

        try:
            repo_list = self.list_repositories()

            if repo_list:
                print(f"\nFollowing repositories will be deleted\n\n")

                for repo_name in repo_list:
                    print(repo_name)

            if repo_list:
                for repo_name in repo_list:
                    Repository(instance=self.instance, user=self.user, key=self.key, repo_name=repo_name).delete_repository()

                    if repo_list.index(repo_name) == len(repo_list) - 1:
                        self.run_post(delete_project)
                        print("Project deleted")
            else:
                self.run_post(delete_project)
                print("Project deleted")

        except:
            raise Exception(f"Could not delete {self.key} on {self.instance}. It may not be exists or {self.user[:self.user.index(':')]} does not have admin permission, or your project is not empty.")


class Repository(Project):

    def __init__(self, instance, user, key, repo_name):
        self.repo_name = repo_name
        super().__init__(instance, user, key)

    def clone(self):

        clone_ = f"https://{self.user}@{self.instance}/scm/{self.key.upper()}/{self.repo_name}.git repos/{self.repo_name}"
        command = f"git clone --mirror {clone_}"

        self.run_post(command)

    def push(self, target_scm):

        push_ = f"https://{self.user}@{target_scm}/scm/{self.key.lower()}/{self.repo_name}.git"
        command = f"git -C repos/{self.repo_name} push {push_} --all"

        self.run_post(command)

    def create_repository(self):

        DICT = dict()
        PROJECT = """{"key":"%s","avatarUrl":"","avatar":"","links":%s}"""%(self.key,DICT)
        DATA = """{"name":"%s","project":%s,"slug":"%s","scmId":"git","links":%s}"""%(self.repo_name,PROJECT,self.repo_name,DICT)

        command = f"curl -u '{self.user}' --request POST --url 'https://{self.instance}/rest/api/latest/projects/{self.key}/repos' --header 'Accept:application/json' --header 'Content-Type:application/json' --data '{DATA}'"

        try:
            self.run_post(command)
        except:
            raise Exception(f"There is a problem occured in creation of {self.repo_name} on {self.instance}.")

    def delete_repository(self):

        REPOSITORY_DELETE_URL = f'https://{self.instance}/rest/api/latest/projects/{self.key}/repos/{self.repo_name}'
        delete_repo = """curl --request DELETE -u %s --url '%s' --header 'Accept:application/json'"""%(self.user, REPOSITORY_DELETE_URL)

        self.run_post(delete_repo)