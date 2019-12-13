#!/bin/bash
dataset=$1
pos=$2
neg=$3
configPath=output/${dataset}/APA/${pos}-${neg}/config.txt
python2 /BioII/lulab_b/jinyunfan/software/dapars/src/DaPars_main.py $configPath
