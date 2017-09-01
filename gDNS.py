#!/usr/bin/python
import sys, json, requests, subprocess

url="https://dns.google.com/resolve"
pType = 'A'
target = 'www.google.com'

if len(sys.argv) > 1:
    target = sys.argv[1]

if len(sys.argv) > 2:
    pType = sys.argv[2]

dnssec = 'true'
if len(sys.argv) > 3:
    dnssec = sys.argv[3]

params = dict(
    name=target,
    type= pType,
    dnssec=dnssec
)

resp = requests.get(url=url, params=params)
data = json.loads(resp.text)

print 'Host, Address'

l = dict(hosts=[], addresses=[], traceroutes=[])

with open("dns.csv") as myfile:
    for a in data[u'Answer']:
        name = a[u'name']
        if name[-1] == '.':
            name=name[:-1]
        l.hosts.append(name)
        l.addresses.append(a[u'data'])
        print name + ", " + a[u'data']
        rt = subprocess.Popen('traceroute '+ a[u'data']).stdout.read()
        l.traceroutes.append(rt)
        myfile.write

