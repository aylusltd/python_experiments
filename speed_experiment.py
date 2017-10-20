#!/usr/bin/python
import sys
import csv
import json

try:
    f = sys.argv[1]
except:
    print "Please specify a file"

TTFA=[]
TTFA_V = []
TTFB=[]
TTFB_V=[]
a_minus_b = []
a_minus_b_v = []

# with open(f) as csv_file:
#     reader = csv.DictReader(csv_file)
#     for row in reader:
#         TTFA.append(float(row["time to first ad"])/1000)
#         TTFB.append(float(row["TTFB"])/1000)

with open(f) as JSON_file:
    obj = json.load(JSON_file)
    for count in range(1,51):
        TTFA.append(float(obj["data"]["runs"][str(count)]["firstView"]["time to first ad"])/1000)
        TTFB.append(float(obj["data"]["runs"][str(count)]["firstView"]["TTFB"])/1000)

for i, time in enumerate(TTFA):
    a_minus_b.append(time - TTFB[i])

TTFA_m = sum(TTFA)/float(len(TTFA))
TTFB_m = sum(TTFB)/float(len(TTFB))
a_minus_b_m = sum(a_minus_b)/float(len(a_minus_b))

for t in TTFA:
    TTFA_V.append((t - TTFA_m)**2)
TTFA_V = sum(TTFA_V)/float(len(TTFA_V))

for t in TTFB:
    TTFB_V.append((t - TTFB_m)**2)
TTFB_V = sum(TTFB_V)/float(len(TTFB_V))


for t in a_minus_b:
    a_minus_b_v.append((t - a_minus_b_m)**2)
a_minus_b_v = sum(a_minus_b_v)/float(len(a_minus_b_v))

print "Time to First Byte (TTFB): "
print "Mean: " + str(TTFB_m) +" Variance: " + str(TTFB_V)

print "Time to First Ad (TTFA): "
print "Mean: " + str(TTFA_m) +" Variance: " + str(TTFA_V)

print "\"Normalized Time to First Ad\" (TTFA - TTFB): "
print "Mean: " + str(a_minus_b_m) +" Variance: " + str(a_minus_b_v)
