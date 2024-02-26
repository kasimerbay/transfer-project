"""
This library is created to transfer projects across Bankalararası Kart Merkezi 's SCM tools.

By Ahmet Kasım Erbay: 20.02.2024 - 16:17:25
"""
import os

class Source:
    def __init__(self, header, scm_url, key, repo_name):
        self.header = header
        self.scm_url = scm_url
        self.key = key
        self.repo_name = repo_name

    def repo(self):

        source_clone = f"{self.header}://{self.scm_url}/scm/{self.key.upper()}/{self.repo_name}.git"

        return source_clone

    def clone_https(self):

        return f"git clone --mirror {Source.repo(self)}"

    def clone_ssh(self):

        return f"git clone ssh://git@{self.scm_url}:7999/{self.key.lower()}/{self.repo_name}.git"

    def change_dir(self, option=True):
        if option:
            return f"cd {self.repo_name}"
        return "cd .."

class Target(Source):

    def __init__(self, header, scm_url, key, repo_name):
        super().__init__(header, scm_url, key, repo_name)


    def push_https(self):

        target_repo = f"{self.header}://{self.scm_url}/scm/{self.key.lower()}/{self.repo_name}.git"

        return f"git push -u {target_repo} --all"

    def push_ssh(self):

        return f"git push -u ssh://git@{self.scm_url}:7999/{self.key.lower()}/{self.repo_name}.git --all"

def definer(string):

    splitted = string.split("/")

    return splitted[0][:-1], splitted[2], splitted[4].lower(), splitted[6].lower()

def get_source_url(url):

    header, scm_url, key, repo_name = definer(url)

    return Source(header, scm_url, key, repo_name)

def get_target_url(url):
    
    header, scm_url, key, repo_name = definer(url)

    return Target(header, scm_url, key, repo_name)

def read_file(file):

    with open(file,"r") as url_file:
        url_list = url_file.readlines()

    return url_list

def write_file(source:Source, target:Target):
    
    with open("transfer.sh", "a", encoding='utf-8') as f:
        print("#!/bin/bash", file=f)

    with open("transfer.sh", "a", encoding='utf-8') as f:
        print(source.clone_ssh(), file=f)
        print(source.change_dir(option=True),file=f)
        print(target.push_https(),file=f)
        print(source.change_dir(option=False),file=f, end="\n")

def create_commands(source_list, target_list):
    if os.path.exists("transfer.sh"):
        os.remove("transfer.sh")

    for i in range(len(source_list)):
        source = get_source_url(source_list[i])
        target = get_target_url(target_list[i])

        write_file(source, target)