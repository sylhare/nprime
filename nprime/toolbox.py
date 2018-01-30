# -*- coding: utf-8 -*-
"""
Created on Mon 27 17:43:39 2017

@author: sylhare

"""
import codecs
import time
import io
import os
import pypandoc
import sys

HERE = os.path.abspath(os.path.dirname(__file__))


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


def read_with_codecs(*parts):
    """Return multiple read calls to different readable objects as a single
    string."""
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


def read_advance(*filenames, **kwargs):
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
    t = time.time()- t

    return t


def convert(markdowm_filepath):
    """Convert a Markdown file to a reStructuredText file with the pypandoc"""
    output = pypandoc.convert(markdowm_filepath, 'rst', outputfile="README.rst")
    return output
