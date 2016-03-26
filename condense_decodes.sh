#!/bin/bash

## by kat gorski / kat.gorski@gmail.com
## code challenge for bit.ly data science internship
## see README.txt for information on this script


touch decode_cond
for NUM in {1..6}
do
    head -n 500000 decodes0$NUM >> decode_cond
done
