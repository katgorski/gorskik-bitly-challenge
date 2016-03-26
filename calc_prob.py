#!/usr/bin/env python3

## by kat gorski / kat.gorski@gmail.com
## code challenge for bit.ly data science internship
## see README.txt for information on this script

import decodes_func as df
from sys import argv

if len(argv) != 4 or argv[1].lower() == 'help':
    print("\nPlease run the script in the following format:")
    print("\tpython3 calc_prob.py MODE QUERY COUNTRY")
    print("Where MODE is the category of the query (domain or link)")
    print("QUERY is the domain or link of interest")
    print("and COUNTRY is the two letter country code of interest.\n")
    quit()

script, mode, query, country = argv
mode = mode.lower().strip()
query = query.lower().strip()

if mode != 'domain' and mode != 'link':
    print("\nPlease use either the term 'domain' or 'link' to ")
    print("communicate the argument of your query.\n")
    quit()



## defining some counters
mobile_count = {'True':0, 'False':0}
query_count = {'True':0, 'False':0}
country_count = dict()
intersect_count = dict()

users = 0

with open("user_db") as f: # make sure you run create_user_db.py first!
    for line in f:
        users += 1
        exec("datum = " + line)
      ## checking to see if from mobile browser
        mobile_bool = df.check_mobile(datum['a'])
        df.increment_dict(mobile_bool, mobile_count)
      ## checking to see if query visited by user
        if mode == 'domain': q = datum['domain'][0]
        elif mode == 'link': q = datum['short_url'][0]
        query_bool = query in q
        df.increment_dict(query_bool, query_count)
      ## checking country code
        df.increment_dict(datum['c'], country_count)
      ## adding intersection to intersect_count
        intersect_key = frozenset(["C:" + datum['c'], "A:" + str(mobile_bool), \
                        "Q:" + str(query_bool), "N:" + str(datum['nk'])])
        df.increment_dict(intersect_key, intersect_count)
        # for debugging: if users == 500: break
        
## now we're getting to the statistics!
## Where c is the country specified in command line and query is the domain/link:
  ## P(query | c)
  ## P(c | query)
  ## P(query | c & mobile)
  ## P(c & mobile | query)
  ## P(mobile | query)

q_int_c = 0
q_int_m = 0
q_int_c_int_m = 0
c_int_m = 0

country_str = "C:" + country
for key in intersect_count:
    if set([country_str, "Q:True"]).issubset(key):
        q_int_c += intersect_count[key]
        if set(["A:True",]).issubset(key):
            q_int_c_int_m += intersect_count[key]
    if set(["A:True", "Q:True"]).issubset(key):
        q_int_m += intersect_count[key]
    if set(["C:" + country, "A:True"]).issubset(key):
        c_int_m += intersect_count[key]

q_int_c /= users
q_int_m /= users
q_int_c_int_m /= users
c_int_m /= users

q_cond_c = q_int_c / (country_count[country] / users)
c_cond_q = q_int_c / (query_count[True] / users)
q_cond_c_and_m = q_int_c_int_m / c_int_m
c_and_m_cond_q = q_int_c_int_m / (query_count[True] / users)
m_cond_q = q_int_m / (mobile_count[True] / users)

print("P(%s | %s)" % (query, country))
print(q_cond_c)
print("P(%s | %s)" % (country, query))
print(c_cond_q)
print("P(%s | %s & mobile)" % (country, query))
print(q_cond_c_and_m)
print("P(%s & mobile | %s)" % (query, country))
print(c_and_m_cond_q)
print("P(mobile | %s)" % query)
print(m_cond_q)
