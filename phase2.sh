#!/bin/bash
chmod +x phase2.sh
sort -u -o prices.txt prices.txt
sort -u -o terms.txt  terms.txt
sort -u -o pdates.txt pdates.txt
sort -u -o ads.txt ads.txt


sed -i 's/:/\n/g' prices.txt
sed -i 's/\\/\\\\/g' prices.txt
sed -i 's/:/\n/g' terms.txt
sed -i 's/\\/\\\\/g' terms.txt
sed -i 's/:/\n/g' pdates.txt
sed -i 's/\\/\\\\/g' pdates.txt
sed -i 's/:/\n/g' ads.txt
sed -i 's/\\/\\\\/g' ads.txt
db_load -c dupsort=1 -f prices.txt -T -t btree pr.idx
db_load -c dupsort=1 -f terms.txt -T -t btree te.idx
db_load -c dupsort=1 -f pdates.txt -T -t btree da.idx
db_load -c dupsort=1 -f ads.txt -T -t hash ad.idx
