"""
Project Atlas

This project is created for project transfer accross SCM Tool instances.
"""

from scm import Project
import sys

def main():

    USER = sys.argv[1]
    KEY = sys.argv[2]
    INSTANCE = sys.argv[3]
    TARGET_SCM = sys.argv[4]


    project = Project(instance=INSTANCE, user=USER, key=KEY)

    project.mirror(TARGET_SCM)


if __name__ == "__main__":
    main()
