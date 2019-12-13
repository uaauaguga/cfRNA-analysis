#!/bin/bash
for cancer in  NC 
do
for selector in SVMRFE ranksum
do
python bin/cross-validation.py \
--input ~/Documents/bioinfo/pico-analysis/variations/expression/matrix/siqi-filter.TMM.txt \
--pos_ids ~/Documents/bioinfo/pico-analysis/sample_ids/strigent-filter/${cancer}.txt \
--neg_ids ~/Documents/bioinfo/pico-analysis/sample_ids/strigent-filter/no-${cancer}.txt \
--feature selected-features/${cancer}-no_${cancer}-${selector}.txt --output CV-RF/${cancer}-no_${cancer}-${selector}.txt
done
done
