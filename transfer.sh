#!/bin/bash
git clone --mirror ssh://git@bitbucket.bkm.com.tr:7999/devops/node-test.git
git -C node-test/ push https://bitbucket-test.bkm.com.tr/scm/devops/node-test.git --all
