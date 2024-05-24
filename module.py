"""
This library is created to transfer projects across Bankalararası Kart Merkezi 's SCM tools.

By Ahmet Kasım Erbay: 20.02.2024 - 16:17:25
"""
import os

class Source:
    def __init__(self, scm_url, key, repo_name, user):

        self.scm_url = scm_url
        self.key = key
        self.repo_name = repo_name
        self.user = user

    def repo(self):

        source_clone = f"https://{self.user}@{self.scm_url}/scm/{self.key.upper()}/{self.repo_name}.git repos/{self.repo_name}"

        return source_clone

    def clone_https(self):

        return f"git clone --mirror {Source.repo(self)}"

    def clone_ssh(self):

        return f"git clone --mirror ssh://git@{self.scm_url}:7999/{self.key.lower()}/{self.repo_name}.git"

    def change_dir(self, option=True):
        if option:
            return f"cd {self.repo_name}"
        return "cd .."

    def introduce_object(self):
        return {
                    "url": self.scm_url, 
                    "key": self.key, 
                    "repo_name": self.repo_name,
                    "repo": self.repo(),
                    "clone_https": self.clone_https(),
                    "clone_ssh": self.clone_ssh(),
                }

class Target(Source):

    def __init__(self, scm_url, key, repo_name, user):
        super().__init__(scm_url, key, repo_name, user)

    def push_https(self):

        target_repo = f"https://{self.user}@{self.scm_url}/scm/{self.key.lower()}/{self.repo_name}.git"

        return f"git -C repos/{self.repo_name} push {target_repo} --all"

    def push_ssh(self):

        target_repo = f"ssh://git@{self.scm_url}:7999/{self.key.lower()}/{self.repo_name}.git"

        return f"git -C {self.repo_name}.git/ push {target_repo} --all"

    def introduce_object(self):
        orig = super().introduce_object()

        orig.update({"push_https": self.push_https(), "push_ssh":self.push_ssh()})

        return orig

def definer(string):

    splitted = string.split("/")

    return splitted[2], splitted[4].lower(), splitted[6].lower()

def get_source_url(url):

    scm_url, key, repo_name = definer(url)

    return Source(scm_url, key, repo_name)

def get_target_url(url):

    scm_url, key, repo_name = definer(url)

    return Target(scm_url, key, repo_name)

def read_file(file):

    with open(file,"r") as url_file:
        url_list = url_file.readlines()

    return url_list

def create_commands(source_list, target_list):

    sources = [get_source_url(i) for i in source_list]
    targets = [get_target_url(i) for i in target_list]

    write_file(sources, targets)

def write_file(sources, targets):

    create_base_file()
    append_sources(sources)
    append_targets(targets)

def create_base_file():
    with open("transfer.sh", "w+", encoding='utf-8') as f:
        print("#!/bin/bash", file=f)

def append_sources(sources):
    with open("transfer.sh", "a", encoding='utf-8') as f:
        for source in sources:
            print(source.clone_https(), file=f)

def append_targets(targets):
    with open("transfer.sh", "a", encoding='utf-8') as f:
        for target in targets:
            print(target.push_https(), file=f)

## Below functions require less file creation

def get_repos(api_call):

    repo_list = []

    for i in range(int(api_call["size"])):
        repo_list.append(api_call["values"][i]["name"])

    return repo_list

def source_scm_call(SOURCE_SCM="bitbucket.bkm.com.tr", KEY="SWC", USER="devops_admin"):

    commands = [
        "touch dels/bitbucket_json.py",
        "echo -n 'repos=' > dels/bitbucket_json.py",
        f"curl -k -u{USER} https://{SOURCE_SCM}/rest/api/1.0/projects/{KEY}/repos?limit=100 >> dels/bitbucket_json.py",
        "sed -i 's/true/True/g' dels/bitbucket_json.py",
        "sed -i 's/false/False/g' dels/bitbucket_json.py"
    ]

    for command in commands:
        if commands.index(command)==2:
            stream = os.popen(command)
            output = stream.read().strip()
            
        else:
            os.popen(command)
    
    print("Your API call successfully done!")
    print("Starting to clone!", end="\n\n")

def clone_repos(source_scm, key, repo_names, user):

    for repo_name in repo_names:

        repo = Source(source_scm, key, repo_name, user)

        try:
            print(f"# Starting to clone {repo.repo_name}")
            print(repo.clone_https())
            command = os.popen(repo.clone_https())
            command.read().strip()
            command.close()
            print()
        except:
            print("There was a problem cloning with {repo.repo_name}")
            print()
            continue

    print("Starting to push all repos...", end="\n\n")

def push_repos(target_scm, key, repo_names, user):

        for repo_name in repo_names:
            repo = Target(target_scm, key, repo_name, user)

            try:
                print(f"# Starting to push {repo.repo_name}")
                print(repo.push_https())
                command = os.popen(repo.push_https())
                command.read().strip()
                command.close()
                print()
            except:
                print("There was a problem pushing with {repo.repo_name}")
                print()
                continue
