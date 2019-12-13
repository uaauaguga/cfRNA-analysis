#!/bin/bash
dataset=$1
pos=$2
neg=$3
if  [ ! -d output/${dataset}/APA/${pos}-${neg} ];then
mkdir -p output/${dataset}/APA/${pos}-${neg}
fi
configPath=output/${dataset}/APA/${pos}-${neg}/config.txt
python bin/prepareDaParConfig.py -d $dataset  -p $pos -n $neg -o $configPath
