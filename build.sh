#!/bin/bash
set -eux

Rscript --vanilla stuff.r
python makehtml.py
rm -rf html/summary_data
cp -r summary_data html

rsync -avz --chmod=Da+rx,a+r --progress html/ summary_data anyall.org:~/www/flightstats/
