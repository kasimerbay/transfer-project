from CONF import Configs

def definer(string):

    splitted = string.split("/")

    return splitted[2], splitted[4].lower(), splitted[6].lower()

def get_source_url(url):

    header, scm_url, key, repo_name = definer(url)

    return Configs(header, scm_url, key, repo_name)

def get_target_url(url):
    header, scm_url, key, repo_name = definer(url)

    return Configs(header, scm_url, key, repo_name)


def clone(source_header, source_scm_url, source_key, source_repo_name):

    source_repo = f"{source_header}://{source_scm_url}/scm/{source_key.lower()}/{source_repo_name}.git"
    return f"git clone {source_repo}"

def push(url, key, repo):
    return f"git push -u https://{url}/scm/{key}/{repo}.git --all"

def linker(from_links:list):
    for i in from_links:
        url, key, repo = definer(i)
        cloner = clone(url, key, repo)
        pusher = push("extbitbucket.bkm.com.tr", key, repo)

        print(cloner)
        print(f"cd {repo}.git")
        print(pusher)
        print("cd ..")
        print()


from_links = [
    "https://bitbucket.bkm.com.tr/projects/DEVOPS/repos/artifactory-scripts/browse"
]


linker(from_links)
