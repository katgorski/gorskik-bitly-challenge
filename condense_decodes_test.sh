#!/bin/bash

## by kat gorski / kat.gorski@gmail.com
## code challenge for bit.ly data science internship
## see README.txt for information on this script

touch decode_cond_alt
for NUM in {1..6}
do
    tail -n 25000 decodes0$NUM >> decode_cond_alt
done
