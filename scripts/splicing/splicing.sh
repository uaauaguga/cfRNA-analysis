#!/bin/bash
dataset=$1
pos=$2
neg=$3
gtfFile=/BioII/lulab_b/jinyunfan/projects/exSEEK/exSeek-dev/genome/hg38/gtf/long_RNA.gtf
rmats_path=/BioII/lulab_b/jinyunfan/software/rMATS.4.0.2/rMATS-turbo-Linux-UCS4/rmats.py
pos_path=output/${dataset}/splicing/no-rmdup/bamPath/${pos}.txt
neg_path=output/${dataset}/splicing/no-rmdup/bamPath/${neg}.txt
outdir=output/${dataset}/splicing/no-rmdup/${pos}-${neg}
mkdir -p ${outdir}
echo ${pos_path}
echo ${neg_path}
python2 ${rmats_path} --b1 ${pos_path} --b2 ${neg_path} --gtf ${gtfFile} --od ${outdir} -t paired  --libType fr-firststrand --readLength 150
