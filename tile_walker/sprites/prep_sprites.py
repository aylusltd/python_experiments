from PIL import Image, ImageTk
from os import listdir
from os.path import isfile, join


import imp

constants = imp.load_source('constants', '../constants.py')

mypath = "./"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and ".gif" in f]
g = constants.grid_size

for img in onlyfiles:
    i = Image.open(img)
    i.thumbnail((g,g))
    i.save("sm_"+img)
