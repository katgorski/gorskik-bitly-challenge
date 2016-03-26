#!/usr/bin/env python3

## by kat gorski / kat.gorski@gmail.com
## code challenge for bit.ly data science internship
## see README.txt for information on this script

multiple = 0
total = 0
with open("user_db") as f:
    for line in f:
        total += 1
        exec("datum = " + line)
        if len({key:1 for key in datum['short_url']}) > 1:
            multiple += 1
print("Number of users with multiple engagements: %s" % multiple)
print("Total number of users: %s" % total)
print("Proportion of users visiting multiple sites: %s" % (multiple/total))
