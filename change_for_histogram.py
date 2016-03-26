#!/usr/bin/env python3

## by kat gorski / kat.gorski@gmail.com
## code challenge for bit.ly data science internship
## see README.txt for information on this script

# Changes the format of the domain_data and short_url files so you
# can use the histogram script from the bit.ly github to visualize
# the distribution of unique link engagements!
# Run as python3 change_for_histogram.py data | histogram_bitly.py

from sys import argv
from re import split
script, data = argv

with open(data) as f:
    for line in f:
        link = split(': ', line)
        sites = split(', ', link[1].strip())
        for x in range(len(sites)): print(link[0].strip())
