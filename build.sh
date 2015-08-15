#!/bin/bash
set -eux

Rscript --vanilla stuff.r
python makehtml.py
