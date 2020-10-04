# -*- coding: utf-8 -*-
"""
Created on Mon 27 17:43:39 2017

@author: sylhare

"""
import codecs
import io
import os
import random
import time

HERE = os.path.abspath(os.path.dirname(__file__))


def crypto_random():
    """ Should print a random for cryptographic use that is not a pseudo random."""
    key_num = random.SystemRandom()
    # key_num.randint(0, sys.maxint) # produces an integer between 0 and the highest allowed by the OS.

    return key_num.random()


# --- FILE --- #
def save(string, name="prime"):
    """
    Write the string into a text file
    The file is called 'name + the time' (format YYYY-mm-dd)

    """
    os.getcwd()

    file = open(str(name) + "_" + str(time.strftime('%Y-%m-%d')) + '.txt', 'w')
    file.write(string)
    file.close()

    return os.path.realpath(file.name)


def read_into_lines_list(path, n=0):
    """
    Take a file and store all of its content into a list
    The n allow to skip the n number of lines

    Return a list of string
    """
    with open(path, 'r') as f:
        content = f.readlines()

    return content[n:]


def read_with_codecs(*parts):
    """Return multiple read calls to different readable objects as a single
    string."""
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


def read_advance(*filenames, **kwargs):
    """

    :param filenames:
    :param kwargs:
    :return:
    """
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


# --- TIME --- #
def timex(func, *param):
    """
    Calculates the time a function takes to run

    Return the function's time
    """
    t = time.time()
    func(*param)
    t = time.time() - t

    return t
