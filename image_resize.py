#!/usr/bin/python
import sys
from PIL import Image
from os.path import join, dirname

mypath = dirname(__file__)
f = sys.argv[1]
n = int(sys.argv[2])

print f
print n

def make_square(im, min_size=512, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, ((size - x) / 2, (size - y) / 2))
    return new_im

full_path = join(mypath,f)
i = Image.open(full_path)
i.thumbnail((n,n))
i = make_square(i)
file_name = f.split('/')[-1:][0]
i.save(join(mypath,"sm_"+file_name))
