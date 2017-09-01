#!/usr/bin/python
import sys
import math
import time
import csv

from primeCheck import check

m = int(sys.argv[1])


start = time.clock()
def sieve(n):
    t = []
    for i in range(1,n):
        t.append(i)
    s = int(math.sqrt(n))
    for i in range(2,s+1):
        for j in t:
            if(j is not None and j>i and j%i==0):
                t[j-1]=None
    return [x for x in t if x is not None]

l=sieve(m)
# for i in l:
#     assert(check(i))

# with open('primes.csv', 'wb') as myfile:
#     wr = csv.writer(myfile)
#     wr.writerow(l)

print l
end = time.clock()

print str(end-start) +"s"