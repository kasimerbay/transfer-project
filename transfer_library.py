"""
This library is created to transfer projects across Bankalararası Kart Merkezi 's SCM tools.

By Ahmet Kasım Erbay: 20.02.2024 - 16:17:25
"""


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

        source_repo = Source.repo(self)

        return f"git clone --mirror {source_repo}"

    def clone_ssh(self):

        return f"git clone ssh://git@{self.scm_url}:7999/{self.key.lower()}/{self.repo_name}.git"

class Target(Source):

    def __init__(self, header, scm_url, key, repo_name):
        super().__init__(header, scm_url, key, repo_name)


    def push_https(self):

        target_repo = f"{self.header}://{self.scm_url}/scm/{self.key.lower()}/{self.repo_name}.git"

        return f"git push -u {target_repo} --all"

    def push_ssh(self):

        target_repo = f"{self.header}://{self.scm_url}/scm/{self.key.lower()}/{self.repo_name}.git"

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

"""
f"git clone --mirror ssh://git@{url}:7999/{key}/{repo}.git"

f"git push -u https://{url}/scm/{key}/{repo}.git --all"

"""