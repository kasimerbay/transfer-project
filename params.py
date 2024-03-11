import sys, argparse

parser = argparse.ArgumentParser(description="Transfer projects across Bitbucket instances with simple interface")


parser.add_argument("--clone_with", "-c", help="'SSH' to use SSH option in from UI.\n'HTTPS' to use HTTPS option from the UI.", type=str)
parser.add_argument("--push_with", "-p", help="'SSH' to use SSH option in from UI.\n'HTTPS' to use HTTPS option from the UI.", type=str)
parser.add_argument("--source_instance", "-S", help="Source Bitbucket instance for cloning")
parser.add_argument("--target_instance", "-T", help="Target Bitbucket instance for pushing")
parser.add_argument("--repo_name", "-R", help="Repoasitory name to be transfered.")


args = parser.parse_args()

print(args)
