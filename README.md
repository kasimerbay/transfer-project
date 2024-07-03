
# Transfer Project Accross Bitbucket Instances

Transfer your project acrross Bitbucket Data Center Instances and interact Bitbucket via Python Interface.

This project is build on [Bitbucket Data Center REST API 2.0](https://developer.atlassian.com/server/bitbucket/rest/).

It uses Python Subprocesses to run REST API ``curl`` options on a Linux VM.

## Use Case

Two seperate Bitbucket Instances; one for Production one for Backup. This script will transfer the specifed project to Backup instance.

![Logo](https://github.com/kasimerbay/kasimerbay.github.io/blob/master/transfer-project.jpeg)

Voala! This is an alternative for Bitbucket Mirror, if it used via cronjob.

## Usage

On your local terminal, add the below environment variables and run the script;

```bash

export USER='<user_name>:<password>'
export KEY='<PROJECT_KEY>'
export SOURCE_SCM=source-bitbucket.<your_domain>.com
export TARGET_SCM=target-bitbucket.<your_domain>.com

./start-transfer.sh $USER $KEY $SOURCE_SCM $TARGET_SCM

```

## Used By

Created for [Interbank Card Center](https://bkm.com.tr/en/).
