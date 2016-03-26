#!/usr/bin/env python3

## by kat gorski / kat.gorski@gmail.com
## code challenge for bit.ly data science internship
## see README.txt for information on this script

import decodes_func as df 

user_dict = dict()

with open("decode_cond") as f:
    for line in f:
        exec("datum = " + line)
        uid = datum["h"]
        if uid not in user_dict:
            user_dict[uid] = dict()
            user_dict[uid]['uid'] = uid
            if 'c' in datum: user_dict[uid]['c'] = datum['c']
            else: user_dict[uid]['c'] = 'undef'
            user_dict[uid]["nk"] = datum["nk"]
            user_dict[uid]['a'] = datum["a"]
        df.append_to_key("short_url", user_dict[uid], datum["g"])
        df.append_to_key("domain", user_dict[uid], df.get_domain(datum["u"]))

with open("user_db", "w") as f:
    for user in user_dict:
        write_str = "{ 'uid':%r, 'c':%r, 'a':%r, 'nk':%r, 'short_url':%r, \
                'domain':%r }\n" % (user_dict[user]['uid'], \
                user_dict[user]['c'], user_dict[user]['a'], \
                user_dict[user]['nk'], user_dict[user]['short_url'], \
                user_dict[user]['domain'])
        f.write(write_str)
