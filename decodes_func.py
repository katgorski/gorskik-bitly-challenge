#!/usr/bin/env python3

## by kat gorski / kat.gorski@gmail.com
## code challenge for bit.ly data science internship
## see README.txt for information on this script

import re
from math import sqrt

def increment_dict(key, dictionary):
    """Attempts to increment dictionary[key] by 1.
    If unsuccessful, assigns 1 to dictionary[key]."""
    try: dictionary[key] += 1
    except KeyError: dictionary[key] = 1
    finally: return

def append_to_key(key, dictionary, item):
    """Attempts to add item to the list dictionary[key].
    If the key is not defined, creates list for dictionary[key]
    cotaining the item passed into the function."""
    try: dictionary[key].append(item)
    except KeyError: dictionary[key] = [item]
    finally: return

def sort_by_count(dictionary):
    """Returns a new dictionary in reverse order with key:value 
    terms of # of engagements : tuple of links with that number
    of engagements, in addition to a reverse sorted list of keys."""
    count_dict = dict()
    for key in dictionary:
        if dictionary[key] in count_dict:
            new_val = tuple([key,] + list(count_dict[dictionary[key]]))
        else: 
            new_val = (key,)
        count_dict[dictionary[key]] = new_val
    val = list(count_dict.keys())
    val.sort(reverse=True)
    return count_dict, val

def write_to_file(filename, dictionary, keys):
    """For dictionaries of the form key:iterable, writes the dictionary
    to file in a readable manner."""
    with open(filename, "w") as f:
        for key in keys:
            f.write(str(key) + ": (")
            for i in range(len(dictionary[key])-1):
                f.write(dictionary[key][i] + ", ")
            f.write(dictionary[key][-1] + ")\n")

def get_domain(long_url):
    """Takes long url and returns just the web domain. 
    This includes any prefixes to the domain, for example,
    https://my.slate.com/subscriptions/podcast/urt619f9
    returns my.slate.com."""
    matches = re.search(r'://(?P<domain>.+?)/', long_url + "/")
    return matches.group('domain')

def get_counts(rev_dict):
    """Returns a list of how many engagements per URL for
    statistical summaries."""
    counts = []
    for key in rev_dict:
        counts += [key] * len(rev_dict[key])
    return counts

def find_basic_stats(counts):
    """Given a list of counts of some arbitrary event, returns the
    average of the data in the list and the standard deviation of
    the items in the list."""
    pass
    average = sum(counts) / len(counts)
    sum_of_sq = 0
    for count in counts:
        sum_of_sq += (count - average) ** 2
    var = sum_of_sq / (len(counts) - 1)
    std = sqrt(var)
    return average, var, std

def check_mobile(a):
    """Given the browser user agent information, determines if it is
    from a mobile browswer, based on the presence of system names
    (Windows Phone, BlackBerry, iPad, iPhone, Android). This will miss
    a handful of mobile browsers, unfortunately."""
    m = re.search(r'iPhone|iPad|BlackBerry|Android|Windows Phone', a) 
    if m: return True
    else: return False

if __name__ == "__main__":
    print("\nThis is decodes_func.py, written by kat gorski for bit.ly.")
    print("Not mean to be run on its own, just used by other files!\n")
    quit()

