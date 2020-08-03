#!/bin/bash
labels=metadata/covariates.txt
for data in APA editing splicing metagenomics;do
for cancer in STAD ESCA HCC LUAD CRC;do
input=variations/${data}.txt
outdir=output-shuffle/${data}/${cancer}-NC
[ -d ${outdir} ] || mkdir -p ${outdir}
bsub -q Z-LU "python  -W ignore bin/classification.py --input ${input} --labels ${labels} --pos ${cancer} --neg NC --model  ${outdir}/model.pickle --performance ${outdir}/performance.txt --roc ${outdir}/roc.txt --features ${outdir}/features.txt 2> log/${data}-${cancer}-NC.txt"
done
outdir=output-shuffle/${data}/pan-cancer-NC
[ -d ${outdir} ] || mkdir -p ${outdir}
bsub -q Z-LU "python  -W ignore bin/classification.py --input ${input} --labels ${labels} --pos CRC,STAD,LUAD,HCC --neg NC --model  ${outdir}/model.pickle --performance ${outdir}/performance.txt --roc ${outdir}/roc.txt --features ${outdir}/features.txt 2> log/${data}-pan-cancer-NC.txt"
done
