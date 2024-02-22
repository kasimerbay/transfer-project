git clone ssh://git@bitbucket.bkm.com.tr:7999/devops/transfer_project.git
cd transfer_project
git push -u https://bitbucket-test.bkm.com.tr/scm/devops/transfer_project.git --all
cd transfer_project
git clone ssh://git@bitbucket.bkm.com.tr:7999/devops/artifactory-scripts.git
cd artifactory-scripts
git push -u https://bitbucket-test.bkm.com.tr/scm/devops/artifactory-scripts.git --all
cd artifactory-scripts
