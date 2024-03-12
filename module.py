"""
This library is created to transfer projects across Bankalararası Kart Merkezi 's SCM tools.

By Ahmet Kasım Erbay: 20.02.2024 - 16:17:25
"""



class Source:
    def __init__(self, scm_url, key, repo_name):

        self.scm_url = scm_url
        self.key = key
        self.repo_name = repo_name

    def repo(self):

        source_clone = f"https://{self.scm_url}/scm/{self.key.upper()}/{self.repo_name}.git"

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

    def __init__(self, scm_url, key, repo_name):
        super().__init__(scm_url, key, repo_name)

    def push_https(self):

        target_repo = f"https://{self.scm_url}/scm/{self.key.lower()}/{self.repo_name}.git"

        return f"git -C {self.repo_name}.git/ push {target_repo} --all"

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
