#! /usr/bin/python
from os.path import isfile, join, realpath, abspath, dirname
from imp import load_source

mypath = dirname(__file__)

print mypath
mp = load_source('mypath', mypath+'/test/imp_check.py')
m = mp.mypath()

print abspath(__file__)
print "m"
# s = m()
print m
