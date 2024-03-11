"""
Project Atlas

This project is created for project transfer accross SCM Tool instances.
"""

from module import *

def main():
    source_list = read_file("source.txt")
    target_list = read_file("target.txt")

    create_commands(source_list, target_list)
    rmtree("__pycache__/")

if __name__ == "__main__":
    main()
