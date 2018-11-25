#!/bin/bash
chmod +x sortScript.sh
sort -u -o prices.txt prices.txt
sort -u -o terms.txt  terms.txt
sort -u -o pdates.txt pdates.txt
sort -u -o ads.txt ads.txt
