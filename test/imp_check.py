from os.path import isfile, join, realpath, abspath, dirname
from imp import load_source


def mypath():
    m = realpath(dirname(__file__))
    return m