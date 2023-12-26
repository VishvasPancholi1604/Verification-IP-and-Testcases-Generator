import os
import argparse

# find project name from path
# extracts project name from the current path
def find_project_name(path, prefix):
    directories = path.split(os.path.sep)
    for i in range(len(directories) - 1, 0, -1):
        if directories[i].startswith(prefix):
            return directories[i][3:]
    return None

# command line argument parser
def get_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-e', '--environment', action='store_true',
                        help='To create more than 1 environment component')
    parser.add_argument('-t', '--testcases', action='store_true',
                        help='to create testcase classes, enter name seperated by comma')
    return parser.parse_args()
