from transfer_library import *

source_url = "https://bitbucket.bkm.com.tr/projects/DEVOPS/repos/artifactory-scripts/browse"
target_url = "https://bitbucket.bkm.com.tr/projects/DEVOPS/repos/transfer_project/browse"

source = get_source_url(source_url)
target = get_target_url(target_url)

print(source.repo())
print(target.push_ssh())