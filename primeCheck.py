#!/usr/bin/python
import sys
import math
import time
import csv

m = sys.argv[1]

def check(n):
    t = []
    s = int(math.sqrt(n))

    retVal = True

    for i in range(2,s+1):
        t.append(i)
    for j in t:
        if(n%j==0 and n>2):
            retVal=False
    return retVal

assert(check(1)==True)
assert(check(2)==True)
assert(check(3)==True)
assert(check(4)==False)
assert(check(5)==True)
assert(check(6)==False)
assert(check(7)==True)
assert(check(8)==False)
assert(check(9)==False)
assert(check(9973)==True)
assert(check(9999991)==True)

# start = time.clock()

# with open(m, 'rb') as myfile:
#     rows = csv.reader(myfile)
#     for row in rows:
#         for val in row:
#             if not check(int(val)):
#                 print str(val) + " is not prime"

# end = time.clock()

# print str(end-start) +"s"