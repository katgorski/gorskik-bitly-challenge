#!/usr/bin/env python3

## by kat gorski / kat.gorski@gmail.com
## code challenge for bit.ly data science internship
## see README.txt for information on this script

import decodes_func as df

intsect_wo_country = dict()
intsect_w_country = dict()
country_count = dict()

## What we want to classify here is what country a user belongs to based on
## what link they clicked, what type of browser they used, and the general 
## domain from the link. This is very simple and likely to not be accurate.
## I know that the decodes provide time zones, but seeing if there was any
## insight to be had based on just the other data available seemed like the
## more interesting problem. 

total_users = 0
with open("user_db") as f: # user_db is the training data set
    for line in f:
        exec("datum = " + line)
        platform = datum['a']
        short_url = datum['short_url'][0] # no users in my training set
        domain = datum['domain'][0]       # had more than one link in history
        country = datum['c']
        nk = datum['nk']
        df.increment_dict(country, country_count)
        w_country_key = frozenset(['A:' + repr(platform), 'C:' + repr(country), \
                        'NK:' + repr(nk), 'S:' + repr(short_url), \
                        'D:' + repr(domain)])
        wo_country_key = frozenset(['A:' + repr(platform), 'NK:' + repr(nk), \
                        'S:' + repr(short_url), 'D:' + repr(domain)])
        df.increment_dict(w_country_key, intsect_w_country)
        df.increment_dict(wo_country_key, intsect_wo_country)
        total_users += 1
        #if total_users == 5000: break // quicker set for debugging

test_users = 0
success = 0
with open("user_db_test") as f:
    for line in f:
        exec("datum = " + line)
        platform = datum['a']
        short_url = datum['short_url'][0] # no users in my training set
        domain = datum['domain'][0]       # had more than one link in history
        country = datum['c']
        nk = datum['nk']
        set_x = frozenset(['A:' + repr(platform), 'NK:' + repr(nk), \
                        'S:' + repr(short_url), 'D:' + repr(domain)])
        try:
            alpha = intsect_wo_country[set_x]
        except KeyError:
            continue
        argmax = 0
        predict_country = ""
        for key in intsect_w_country:
            if set_x.issubset(key):
                argtemp = alpha * (intsect_w_country[key] / total_users)
                if argtemp > argmax: # not dealing with multiple possibilities
                    argmax = argtemp
                    for item in key:
                        if item[:2] == 'C:': 
                            predict_country = item[3:-1]
                            break
        if argmax == 0: continue
        print("Actual country: %s, predicted country: %s" % (country, predict_country))
        if (country == predict_country): success += 1
        test_users += 1
        #if test_users == 500: break // only a few tests for debugging

print("Percent correct: %f" % ((success / test_users) * 100))
