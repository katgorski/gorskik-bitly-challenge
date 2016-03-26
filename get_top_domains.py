#!/usr/bin/env python3

## by kat gorski / kat.gorski@gmail.com
## code challenge for bit.ly data science internship
## see README.txt for information on this script

import decodes_func as df
from math import floor, ceil

short_url_count = dict()
domain_count = dict()
user_dict = dict() # to keep to unique hits

#total_decodes = 0

with open("decode_cond") as f:
    for line in f:
#        total_decodes += 1
        exec("datum = " + line)
        
        ## To make sure we are getting UNIQUE hits
        try: 
            if datum["g"] in user_dict[datum["h"]]:
                unique = False
        except KeyError:
            unique = True
            df.append_to_key(datum["h"], user_dict, datum["g"])
        if unique == False: continue

        domain = df.get_domain(datum["u"])
        df.increment_dict(domain, domain_count)
        df.increment_dict(datum["g"], short_url_count)
#        if total_decodes == 25000: break

rev_domain_count, domain_counts = df.sort_by_count(domain_count)
rev_link_count, link_counts = df.sort_by_count(short_url_count)

df.write_to_file('domain_counts', rev_domain_count, domain_counts)
df.write_to_file('short_url_counts', rev_link_count, link_counts)

# Determining some basic statistics:
    # Average and standard deviation of engagements for a domain
    # Average and standard deviation of engagements for a link
# writes to output file summary_statistics.txt

with open("summary_statistics.txt", "w") as f:
    f.write("SHORT URL STATISTICS\n")
    f.write("Top ten links (unique hits):\n")
    for i in range(len(link_counts)):
        if i >= 10: break
        f.write(str(link_counts[i]) + ": ")
        write_count = 0
        for link in rev_link_count[link_counts[i]]:
            f.write(link + " ")
            write_count += 1
            if write_count >= 10:
                f.write("...")
                break
        f.write("\n")
    f.write("Summary statistics:\n")
    average, var, std = df.find_basic_stats(df.get_counts(rev_link_count))
    f.write("Average: %.3f\n" % average)
    f.write("Variance: %.3f\n" % var)
    f.write("Standard deviation: %.3f\n" % std)

    f.write("\nDOMAIN STATISTICS\n")
    f.write("Top ten domains (unique hits):\n")
    for i in range(len(domain_counts)):
        if i >= 10: break
        f.write(str(domain_counts[i]) + ": ")
        for link in rev_domain_count[domain_counts[i]]:
            f.write(link + " ")
        f.write("\n")
    f.write("Summary statistics:\n")
    average, var, std = df.find_basic_stats(df.get_counts(rev_domain_count))
    f.write("Average: %.3f\n" % average)
    f.write("Variance: %.3f\n" % var)
    f.write("Standard deviation: %.3f\n" % std)
