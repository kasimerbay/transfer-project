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
                Project(instance=self.instance, user=self.user, key=key).delete_project()
            except:
                undeleted_projects.append(key)

        if len(undeleted_projects) != 0:
            print(f"\nList of undeleted projects in {self.instance}:\n")
            for key in undeleted_projects:
                print(key)

    def delete_all_groups(self):
        group_list = Instance(instance=self.instance, user=self.user).list_all_groups()

        undeleted_groups = []

        for group_name in group_list:
            if group_name != 'stash-users' and group_name != 'DevOps':
                try:
                    Group(instance=self.instance, user=self.user, group_name=group_name).delete_group()
    
                except:
                    undeleted_groups.append(group_name)
            else:
                undeleted_groups.append(group_name)

        if len(undeleted_groups) != 0:
            print(f"\nList of undeleted groups in {self.instance}:\n")
            for group_name in undeleted_groups:
                print(group_name)

    def delete_users(self, user_list):

        existing_users = Instance(instance=self.instance, user=self.user).user_list()
        undeleted_users = []

        for user in existing_users:
            if user[0] in user_list and user[0] != 'devops_admin':
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

    def list_all_projects_repos(self):

        repo_list = {}

        for key in Instance(instance=self.instance, user=self.user).list_projects():
            repo_list.update({key:Project(instance=self.instance, user=self.user, key=key).list_repositories()})

        return repo_list

class Instance:
    def __init__(self, instance, user):
        self.instance = instance
        self.user = user

    def api_to_json(self, api_call):
        """Returns Json formatted API Call to SCM

            This is a complementary function for API Call
        Args:
            api_call (_type_): Curl command string result to be formatted to Dict

        Raises:
            Exception: If the user has no permission on target object

        Returns:
            Dict: Formatted dictionary object from API Call
        """
        words = {"true":"True", "false":"False"}

        for key,value in words.items():
            api_call = api_call.replace(key, value)

        try:
            api_call = eval(api_call)
        except:
            raise Exception(f"Please be sure {self.user[:self.user.index(':')]} has right permissions in {self.key} on {self.instance}.\nOr this means your api_call returned an empty string.")

        return api_call

    def run(self, command):
        """Run on system with Git installed

        Args:
            command (string): git command to be run

        Returns:
            None: _
        """
        print(command)
        return subprocess.run(command.split(" "), cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")

    def run_post(self, command):
        """Run on system with git

        Args:
            command (string): git command to be run. This command runs on a Linux OS.

        Returns:
            String: String to be sent to api_to_json method.
        """
        print(command)
        stream = os.popen(command)
        output = stream.read().strip()
        print(output)
        return output

    def list_projects(self):
        """List project keys in an Bitbucket Instance

        Returns:
            List(string): List of project keys in the instance
        """
        command = f"curl -k -u'{self.user}' https://{self.instance}/rest/api/1.0/projects?limit=100"

        api_call = self.run_post(command)
        api_call = self.api_to_json(api_call)

        return [api_call["values"][i]["key"] for i in range(int(api_call["size"]))]

    def project_list(self):
        """List of API calls to projects

        Returns:
            List(string): List of API calls to projects. This method is a powerset of list_projects method.
        """
        list_projects = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/projects?limit=200' --header 'Accept:application/json' """

        api_call = self.run_post(list_projects)
        api_call = self.api_to_json(api_call)

        projects = [api_call["values"][i] for i in range(int(api_call["size"]))]
        return [(projects[i]["key"], projects[i]["name"], projects[i]["id"]) for i in range(len(projects))]

    def list_all_groups(self):
            """ List all groups in a Bitbucket Instance
            
            Returns:
                List(string): List of all the group names in a Bitbucket Instance
            """
            list_groups = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/admin/groups?limit=1600' --header 'Accept:application/json' """
            api_call = self.run_post(list_groups)
            api_call = self.api_to_json(api_call)

            groups = [api_call["values"][i]["name"] for i in range(int(api_call["size"]))]

            return groups

    def list_users(self):
        """List all users in a Bitbucket Instance
        
        Returns:
            List(string): List of all users in a Bitbucket Instance
        """
        command = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/users?limit=1000' --header 'Accept:application/json'"""

        api_call = self.run_post(command)
        api_call = self.api_to_json(api_call)

        return [api_call["values"][i]["name"] for i in range(int(api_call["size"]))]

    def user_list(self):
        """List of API calls to users

        Returns:
            List(string): List of API calls to users. This method is a powerset of list_users method.
        """
        command = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/users?limit=1000' --header 'Accept:application/json'"""

        api_call = self.run_post(command)
        api_call = self.api_to_json(api_call)

        users = [api_call["values"][i] for i in range(int(api_call["size"]))]

        return [(user["name"], user["displayName"], user["emailAddress"]) for user in users]

    def create_groups(self):
        """Create ideal groups based on project keys in an Instance

            This method is an ideal method to standardize a Bitbucket Instance. It create groups with 
            <KEY>_ADMIN, <KEY>_WRITE and <KEY>_READ for all the groups in the Instance. This groups
            is to be privilaged for the <KEY> project, accordingly.

        Returns:
            None: _
        """
        project_list = self.list_projects()

        for project_key in project_list:
            group_names = [project_key + "_ADMIN", project_key + "_WRITE", project_key + "_READ"]
            for group_name in group_names:
                Group(instance=self.instance, user=self.user, group_name=group_name).create_group()

    def give_group_permissions(self):
        """Give ideal group permissions to projects.

            Based on the groups created by create_groups() method, give permissions to these groups accordingly.

        Returns:
            None: _
        """
        projects = Instance(instance=self.instance, user=self.user).list_projects()
        self.create_groups()

        for project in projects:
            Project(instance=self.instance, user=self.user, key=project).give_group_permission()

class Group(Instance):
    def __init__(self, instance, user, group_name):
        self.group_name = group_name
        super().__init__(instance, user)

    def create_group(self):
        """Create a group from Group object
        
        Returns:
            None: _
        """

        create_group = f"""curl -u'{self.user}' --request POST --url 'https://{self.instance}/rest/api/latest/admin/groups?name={self.group_name}' --header 'Accept:application/json' -H "X-Atlassian-Token:no-check" """

        self.run_post(create_group)

    def delete_group(self):
        """Delete a group

        Returns:
            None: _
        
        """
        delete_group = f"""curl -u'{self.user}' --request DELETE --url 'https://{self.instance}/rest/api/latest/admin/groups?name={self.group_name}' --header 'Accept:application/json' -H "X-Atlassian-Token:no-check" """

        self.run_post(delete_group)

    def mirror_all_groups(self, target_scm):
        """Mirror or transfer all the groups within a Bitbucket Instance to another Bitbucket Instance

        Args:
            target_scm (String): Domain name for your Bitbucket Instance.
                Example: "bitbucket-prod.example.com"
        """
        group_list_source = self.list_all_groups()
        group_list_target = Instance(instance=target_scm, user=self.user).list_all_groups()

        untransferred_groups = []

        for group_name in group_list_source:
            if group_name not in group_list_target:
                try:
                    Group(instance=target_scm, user=self.user, group_name=group_name).create_group()
                except:
                    untransferred_groups.append(group_name)
            else:
                untransferred_groups.append(group_name)

        print(f"\nList of untransferred groups:\n")
        for group_name in untransferred_groups:
            print(group_name)

    def list_all_group_permissions(self):
        """List all groups with matching permissions for all the groups in an instance

        Returns:
            Dict(Dict): Dictionary of {<KEY>:{<GROUP>:<PERMISSON>}} 
        """
        projects = self.list_projects()
        group_permissions = {}

        for key in projects:
            group_permissions.update({key:Project(instance=self.instance, user=self.user, key=key).list_group_permission()})

        return group_permissions

class User(Instance):
    def __init__(self, instance, user, name, display_name, email):
        self.name = name
        self.display_name = display_name
        self.email = email
        self.password = "changeme123"
        super().__init__(instance, user)

    def create_user(self):
        """Create a user in a given instance
        
        Returns:
            None: _
        """
        create_user = f"""curl -u'{self.user}' --request POST --url 'https://{self.instance}/rest/api/latest/admin/users?emailAddress={self.email}&password={self.password}&displayName={self.display_name}&name={self.name}' -H "X-Atlassian-Token:no-check" """

        self.run_post(create_user)

    def delete_user(self):
        """Delete a user
        
        Returns:
            None: _
        """
        delete_user = f"""curl -u'{self.user}' --request DELETE --url 'https://{self.instance}/rest/api/latest/admin/users?name={self.name}' --header 'Accept:application/json' """

        self.run_post(delete_user)

    def mirror_all_users(self, target_scm):
        """Mirror or transfer all users in a Bitbucket instance to another.

        Args:
            target_scm (String): https address of the Instance

        Raises:
            Exception: User creation failure
        """
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
        """List repositories in a given project

        Returns:
            List(String): List of repository names in the project
        """
        list_repositories = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/projects/{self.key}/repos?limit=100' --header 'Accept:application/json' """
        try:
            api_call = self.run_post(list_repositories)
            api_call = self.api_to_json(api_call)

            return [api_call["values"][i]["name"] for i in range(int(api_call["size"]))]
        except:
            return []

    def user_permissions(self):
        """List of user names and permissions in a project

            This method lists individual users that has permissions as user not involved in a group!

            Returns:
                List(list): List of name and permission pair in a list
        
        """
        project_user_permissions = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/projects/{self.key}/permissions/users' --header 'Accept:application/json'"""

        api_call = self.run_post(project_user_permissions)
        api_call = self.api_to_json(api_call)

        return [(api_call["values"][i]["user"]["name"],api_call["values"][i]["permission"]) for i in range(int(api_call["size"]))]

    def mirror_repos(self, repo_list:list, target_scm):
        """Mirror or transfer individual repositories accross Bitbucket Instances

        Args:
            repo_list (list): list of repositories that are subject to transfer
            target_scm (String): https address of target instance
        """
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

        untracked_repos = []

        for repo_name in repo_list:
            if repo_name not in untracked_repos:
                try:
                    repo = Repository(self.instance, self.user, self.key, repo_name)
                    repo.clone()
                    repo.push(target_scm=target_scm)
                except:
                    error_list.append(f"{repo_name} -- " + "Clone or Push Error!")
                    continue
            else:
                error_list.append(f"{repo_name} -- " + "Repository is told as not to be transfered")


        if len(error_list)!= 0:
            print("\n\n------ List of untransferred repositories:")
            for error_repo in error_list:
                print("* ", error_repo)
            print(f"Total: {len(error_list)}")

    def mirror(self, target_scm):
        """Mirror or tansfer an entire project

        Args:
            target_scm (String): https address of target instance

        Returns:
            _type_: _description_
        """
        repository_list = self.list_repositories()

        return self.mirror_repos(repo_list=repository_list, target_scm=target_scm)

    def create_project(self):
        """Create project for given Project object
        
        Exception:
            Project creation failure
        """

        PROJECT_URL = f'https://{self.instance}/rest/api/latest/projects'
        DICT = dict()
        create_project = """curl --request POST -u '%s' --url '%s' --header 'Accept:application/json' --header 'Content-Type:application/json' --data '{"key":"%s","avatarUrl":"","avatar":"","links": %s}'"""%(self.user, PROJECT_URL, self.key ,DICT)

        try:
            self.run_post(create_project)
        except:
            raise Exception(f"Could not create {self.key} on {self.instance}.")

    def delete_project(self):
        """Delete an entire project
        
            This method deletes all the repositories along with the container project
        """
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

    def list_group_permission(self):
        """List groups and permissions assigned to a project
        
        Returns:
            List(list): List of group and permission pair list for a project
        """
        project_group_permissions = f"""curl -u'{self.user}' --request GET --url 'https://{self.instance}/rest/api/latest/projects/{self.key}/permissions/groups?limit=300' --header 'Accept:application/json' """

        api_call = self.run_post(project_group_permissions)
        api_call = self.api_to_json(api_call)

        return [(api_call["values"][i]["group"]["name"],api_call["values"][i]["permission"]) for i in range(int(api_call["size"]))]

    def give_group_permission(self):
        """Create ideal groups for a project
        
        Returns:
            None: _
        """
        groups = Instance(instance=self.instance, user=self.user).list_all_groups()

        PERMISSIONS = ["PROJECT_ADMIN", "PROJECT_WRITE", "PROJECT_READ"]
        GROUP_NAMES = [self.key + "_ADMIN", self.key + "_WRITE", self.key + "_READ"]

        unadded_groups = []

        for group_permission in zip(GROUP_NAMES, PERMISSIONS):
            if group_permission[0] in groups:
                group_project_permission = f"""curl -u'{self.user}' --request PUT --url 'https://{self.instance}/rest/api/latest/projects/{self.key}/permissions/groups?name={group_permission[0]}&permission={group_permission[1]}' """

                try:
                    self.run_post(group_project_permission)
                except:
                    unadded_groups.append(group_permission)
            else:
                unadded_groups.append(group_permission)

        if len(unadded_groups) != 0:
            print(f"These are the groups that could not be added to project {self.key}.")
            for group_permission in unadded_groups:
                print(group_permission)

            print("\nCheck if project KEY is right. Or the groups exist")

    def mirror_groups(self, target_scm):
        """Mirror or transfer all the groups within a project to another Bitbucket instance

        Args:
            target_scm (String): Domain name for your Bitbucket Instance.
                Example: "bitbucket-prod.example.com"
        """
        source_project_groups = self.list_group_permission()
        target_project_groups = Project(instance=target_scm, user=self.user, key=self.key).list_group_permission()

        untransferred_groups = []

        for group in source_project_groups:
            if group not in target_project_groups:
                try:
                    Group(instance=target_scm, user=self.user, group_name=group[0]).create_group()
                except:
                    untransferred_groups.append(group[0])
            else:
                untransferred_groups.append(group[0])
        
        if len(untransferred_groups) != 0:
            print()
            print("These are the groups that are not transferred;", end="\n")
            for group in untransferred_groups:
                print(group[0])
            print()

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
        command = f"git -C repos/{self.repo_name} push --force {push_} --all"

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
