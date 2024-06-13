"""
This library is created to transfer projects across Bankalararası Kart Merkezi 's SCM tools.

By Ahmet Kasım Erbay: 20.02.2024 - 16:17:25
"""

import subprocess,os


class Admin:
    def __init__(self, instance, user):
        self.instance = instance
        self.user = user

    def delete_all_projects(self):

        project_keys = Instance(instance=self.instance, user=self.user).list_projects()
        undeleted_projects = []

        for key in project_keys:
            try:
                Project(instance=self.instance, key=key, user=self.user).delete_project()
            except:
                undeleted_projects.append(key)

        print(f"\nList of undeleted projects in {self.instance}:\n")
        for key in undeleted_projects:
            print(key)

    def delete_all_groups(self):
        group_list = Instance(instance=self.instance, user=self.user).list_groups()

        undeleted_groups = []

        for group_name in group_list:
            if group_name != 'stash-users':
                try:
                    Group(instance=self.instance, user=self.user, group_name=group_name).delete_group()
                    
                except:
                    undeleted_groups.append(group_name)
            else:
                undeleted_groups.append(group_name)

        print(f"\nList of undeleted groups in {self.instance}:\n")
        for group_name in undeleted_groups:
            print(group_name)
        pass

    def delete_users(self, user_list):

        existing_users = Instance(instance=self.instance, user=self.user).user_list()
        undeleted_users = []

        for user in existing_users:
            if user[0] in user_list:
                try:
                    User(instance=self.instance, user=self.user, name=user[0], display_name=user[1], email=user[2]).delete_user()
                except:
                    undeleted_users.append(user[0])
            else:
                undeleted_users.append(user[0])

        print(f"\nList of undeleted users in {self.instance}:\n")
        for user_name in undeleted_users:
            print(user_name)

    def delete_all_users(self):
        pass


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
            raise Exception(f"Please be sure {self.user[:self.user.index(':')]} has right permissions in {self.key} on {self.instance}.\nOr this means your api_call returned an empty string.")

        return api_call

    def run(self, command):
        print(command)
        return subprocess.run(command.split(" "), cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")

    def run_post(self, command):
        print(command)
        stream = os.popen(command)
        output = stream.read().strip()
        print(output)
        return output

    def list_projects(self):

        command = f"curl -k -u'{self.user}' https://{self.instance}/rest/api/1.0/projects?limit=100"

        api_call = self.run_post(command)
        api_call = self.api_to_json(api_call)

        return [api_call["values"][i]["key"] for i in range(int(api_call["size"]))]

    def project_list(self):
        command = f"curl -k -u'{self.user}' https://{self.instance}/rest/api/1.0/projects?limit=100"

        api_call = self.run_post(command)
        api_call = self.api_to_json(api_call)

        projects = [api_call["values"][i] for i in range(int(api_call["size"]))]
        return [(projects[i]["key"], projects[i]["name"]) for i in range(len(projects))]

    def list_groups(self):

            list_groups = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/admin/groups?limit=800' --header 'Accept:application/json' """
            api_call = self.run_post(list_groups)
            api_call = self.api_to_json(api_call)

            groups = [api_call["values"][i]["name"] for i in range(int(api_call["size"]))]

            return groups

    def list_users(self):
        command = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/users?limit=1000' --header 'Accept:application/json'"""

        api_call = self.run_post(command)
        api_call = self.api_to_json(api_call)

        return [api_call["values"][i]["name"] for i in range(int(api_call["size"]))]

    def user_list(self):
        command = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/users?limit=1000' --header 'Accept:application/json'"""

        api_call = self.run_post(command)
        api_call = self.api_to_json(api_call)

        users = [api_call["values"][i] for i in range(int(api_call["size"]))]

        return [(user["name"], user["displayName"], user["emailAddress"]) for user in users]


class Group(Instance):
    def __init__(self, instance, user, group_name):
        self.group_name = group_name
        super().__init__(instance, user)

    def create_group(self):

        create_group = f"""curl -u'{self.user}' --request POST --url 'https://{self.instance}/rest/api/latest/admin/groups?name={self.group_name}' --header 'Accept:application/json' -H "X-Atlassian-Token:no-check" """

        self.run_post(create_group)

    def delete_group(self):
        
        delete_group = f"""curl -u'{self.user}' --request DELETE --url 'https://{self.instance}/rest/api/latest/admin/groups?name={self.group_name}' --header 'Accept:application/json' -H "X-Atlassian-Token:no-check" """

        self.run_post(delete_group)

    def mirror_groups(self, target_scm):
        group_list_source = self.list_groups()
        group_list_target = Instance(instance=target_scm, user=self.user).list_groups()

        untransferred_groups = []

        for group_name in group_list_source:
            if group_name not in group_list_target:
                try:
                    Group(instance=self.instance, user=self.user, group_name=group_name).create_group()
                except:
                    untransferred_groups.append(group_name)
            else:
                untransferred_groups.append(group_name)

        print(f"\nList of untransferred groups:\n")
        for group_name in untransferred_groups:
            print(group_name)


class User(Instance):
    def __init__(self, instance, user, name, display_name, email):
        self.name = name
        self.display_name = display_name
        self.email = email
        self.password = "changeme123"
        super().__init__(instance, user)

    def create_user(self):
        create_user = f"""curl -u'{self.user}' --request POST --url 'https://{self.instance}/rest/api/latest/admin/users?emailAddress={self.email}&password={self.password}&displayName={self.display_name}&name={self.name}' -H "X-Atlassian-Token:no-check" """

        self.run_post(create_user)

    def delete_user(self):
        delete_user = f"""curl -u'{self.user}' --request DELETE --url 'https://{self.instance}/rest/api/latest/admin/users?name={self.name}' --header 'Accept:application/json' """

        self.run_post(delete_user)

    def mirror_users(self, target_scm):

        user_list_source = Instance(instance=self.instance, user=self.user).user_list()
        user_list_target = Instance(instance=target_scm, user=self.user).list_users()

        untransferred_users = []

        for user in user_list_source:
            if user[0] not in user_list_target:
                try:
                    User(instance=target_scm, user=self.user, name=user[0], email=user[1], display_name="".join(user[2].split(" "))).create_user()
                except:
                    untransferred_users.append(user[0])
                    raise Exception(f"Could not create user {user[0]} in {target_scm}")
            else:
                untransferred_users.append(user[0])

        print("\nUsers that are not transferred here;", end="\n")
        print(f"They are either already exist in {target_scm}, or contact your admin!", end="\n")

        for name in untransferred_users:
            print(name)
     

class Project(Instance):
    def __init__(self, instance, user, key):
        self.key = key
        super().__init__(instance, user)

    def list_repositories(self):
        command = f"curl -k -u{self.user} https://{self.instance}/rest/api/1.0/projects/{self.key}/repos?limit=100"
        try:
            api_call = self.run_post(command)
            api_call = self.api_to_json(api_call)

            return [api_call["values"][i]["name"] for i in range(int(api_call["size"]))]
        except:
            return []

    def get_project_group_permissions(self):
        
        project_group_permissions = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/projects/{self.key}/permissions/groups?limit=300' --header 'Accept:application/json' """

        api_call = self.run_post(project_group_permissions)
        api_call = self.api_to_json(api_call)

        return [(api_call["values"][i]["group"]["name"],api_call["values"][i]["permission"]) for i in range(int(api_call["size"]))]

    def get_project_user_permissions(self):
        
        project_user_permissions = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/projects/{self.key}/permissions/users' --header 'Accept:application/json'"""

        api_call = self.run_post(project_user_permissions)
        api_call = self.api_to_json(api_call)

        return [(api_call["values"][i]["user"]["name"],api_call["values"][i]["permission"]) for i in range(int(api_call["size"]))]

    def mirror_repos(self, repo_list, target_scm):

        target = Project(instance=target_scm, user=self.user, key=self.key)

        error_list = []
        # If target does not have the project, this for loop creates the project
        target_projects = target.list_projects()

        if target.key not in target_projects:
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
                    print("* ",repo_name)

            if repo_list:
                for repo_name in repo_list:
                    Repository(instance=self.instance, user=self.user, key=self.key, repo_name=repo_name).delete_repository()

                    if repo_list.index(repo_name) == len(repo_list) - 1:
                        self.run_post(delete_project)
                        print("Project deleted")
            else:
                self.run_post(delete_project)
                print(f"{self.key} deleted")

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