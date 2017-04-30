# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 18:50:13 2017

@author: sylhare
@source: http://stackoverflow.com/questions/5411603/how-to-remove-trailing-whitespace-in-code-using-another-script

"""

import os
import sys


def main():
    """
    Parse arguments, then fix whitespace in the given file

    """
    if len(sys.argv) == 1:
        print("All '.py' file from directory will be trimmed")
        path = os.getcwd()
        for path, dirs, files in os.walk(path):
            for file in files:
                if file[-3:] == '.py':
                    rm_trailing_space(file)
                    print("[ OK ] " + file)
                else:
                    print("[FAIL] " + file + " is not a '.py' file")
    else:
        path = sys.argv[1]
        if os.path.exists(path):
            rm_trailing_space(path)
        else:
            print("file not found: %s" % sys.argv[1])
            sys.exit(1)

def main_reboot():
    path = os.getcwd()
    print(path)
    for path, dirs, files in os.walk(path):
        for file in files:
            if file[-3:] == '.py':
                rm_trailing_space(file)
                print("[ OK ] " + file)


def user_input():
    yes = set(['yes','y', 'yup', ''])
    no = set(['no','n'])

    while True:
        print("continue? [y\n]")
        choice = input().lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'")


def rm_trailing_space(path):
    """
    Remove all trailing space from the file of the path

    """
    with open(path, 'r') as file:
        new = [line.rstrip() for line in file]
    with open(path, 'w') as file:
        [file.write('%s\n' % line) for line in new]


if __name__ == "__main__":
    main_reboot()
