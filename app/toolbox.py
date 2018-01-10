# -*- coding: utf-8 -*-
"""
Created on Mon 27 17:43:39 2017

@author: sylhare

"""
import time
import os


# --- FILE --- #
def save(string, name="prime"):
    """
    Write the string into a text file
    The file is called 'name + the time' (format YYYY-mm-dd)

    """
    os.getcwd()

    file = open(str(name) +  "_" + str(time.strftime('%Y-%m-%d')) + '.txt', 'w')
    file.write(string)
    file.close()

    return os.path.realpath(file.name)


def read(path, n=0):
    """
    Take a file and store all of its content into a list
    The n allow to skip the n number of lines

    Return a list of string
    """
    content = []
    with open(path, 'r') as file:
        content = file.readlines()

    return content[n:]


# --- TIME --- #
def timex(func, *param):
    """
    Calculates the time a function takes to run

    Return the function's time
    """
    t = time.time()
    func(*param)
    t = time.time()- t

    return t
