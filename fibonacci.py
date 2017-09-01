#!/usr/bin/python

def fibonacci(n):
    prev=0
    current=1
    fib=[];
    for i in range(0,n):
        fib.append(current);
        current += prev;
        prev = fib[i];
    return fib

import sys

print   fibonacci(int(sys.argv[1]))