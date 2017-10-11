import pprint
import math
import json

def makePos(row, column, width):
    return (row * width) + column

def make_confs(height=4, width=4, length=3):
    win_confs=[]
    win_confs_obj = {
        "all" : []
    }
    if width > height:
        max_dim = "width"
        max_size = width
    else:
        max_dim="height"
        max_size = height

    if max_size < length:
        return win_confs

    j=0
    while j+length <= height:    
        for n in range(0,width):
            # vertical confs
            win = []
            for i in range(0,length):
                win.append(n + ((i+j)*width))
            win_confs.append(win)
        j+=1
    win_confs_obj["vertical"] = win_confs
    win_confs_obj["all"]+=(win_confs)
    win_confs=[]
    j=0
    while width >= length + j:
        for n in range(0,height):
            # horizontal wins
            win=[]
            for i in range(0,length):
                win.append(n*width + i + j)
            win_confs.append(win)
        j+=1
    win_confs_obj["horizontal"] = win_confs
    win_confs_obj["all"]+=(win_confs)
    win_confs = []

    # diagonal wins (top left)
    j=0
    while height >= length +j:
        k=0
        while width >= length +k:
            win=[]
            for i in range(0,length):
                win.append(makePos(row=j+i, column=k+i, width=width))
            win_confs.append(win)
            k+=1
        j+=1
    win_confs_obj["diagonal"] = win_confs
    win_confs_obj["all"]+=(win_confs)
    win_confs = []

    # diagonal wins (top right)
    j=0
    while height >= length +j:
        k=0
        while width >= length +k:
            win=[]
            for i in range(0,length):
                win.append(makePos(row=j+i, column=width-(k+i)-1, width=width))
            win_confs.append(win)
            k+=1
        j+=1
    win_confs_obj["diagonal"]+=(win_confs)
    win_confs_obj["all"]+=(win_confs)
    return win_confs_obj


def make_spaces(val, max_val):
    if val > 0:
        digits = int(math.log(val,10))+1
    elif val == 0:
        digits = 1
    else:
        digits = int(math.log(-val,10))+2
    max_digits = int(math.log(max_val,10)) + 1

    s = str(val)
    for i in range(0, max_digits-digits):
        s=" " + s

    return s

def print_ref_grid(height=4, width=4):
    print ""
    ref = []
    max_val = height * width - 1

    for c in range(0,height):
        r=[]
        for i in range(0,width):
            x=i+ c*width
            x=make_spaces(val=x, max_val=max_val)
            r.append("[  " + x + "  ]")
        ref.append(r)
        print r

# print_ref_grid(height = 17, width=6)
# pprint.pprint(make_confs(height = 17, width=6, length=4))

all_confs = {}
for h in range(3,7):
    all_confs[h] = {}
    for w in range(3,7):
        all_confs[h][w] = {}
        for l in range(3,7):
            if l <= h or l<=w:
                confs=make_confs(height = h, width=w, length=l)
                all_confs[h][w][l] = confs

with open('win_confs.json','w') as f:
    json.dump(all_confs,f, sort_keys=True, indent=4)

