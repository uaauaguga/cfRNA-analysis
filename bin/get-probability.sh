#!/bin/bash
labels=metadata/covariates.txt
for var in expression splicing APA editing metagenomics endo-extra RNA-variations all-features;do
for cancer in CRC STAD HCC LUAD;do
[ -d output/binary-integration/${var}-${cancer} ] || mkdir -p output/binary-integration/${var}-${cancer}
bsub -q Z-LU "python bin/classification-selected.py --input variations-merged.txt --features output/binary-features/${var}/${cancer}.txt --pos ${cancer} --neg NC  --labels ${labels} -proba output/binary-integration/${var}-${cancer}/prob.txt --roc output/binary-integration/${var}-${cancer}/roc.txt --auroc output/binary-integration/${var}-${cancer}/auroc.txt 2>> errrrrrrrrr.log"
done
[ -d output/binary-integration/${var}-pan-cancer ] || mkdir -p output/binary-integration/${var}-pan-cancer
bsub -q Z-LU  "python bin/classification-selected.py --input variations-merged.txt --features output/binary-features/${var}/pan-cancer.txt --pos CRC,STAD,LUAD,HCC --neg NC  --labels ${labels} -proba output/binary-integration/${var}-pan-cancer/prob.txt --roc output/binary-integration/${var}-pan-cancer/roc.txt --auroc output/binary-integration/${var}-pan-cancer/auroc.txt"
done
