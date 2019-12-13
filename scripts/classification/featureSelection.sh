#!/bin/bash
for selector in ranksum SVMRFE
do
for classifier in SVM #RF
do
for cancer in NC #CRC STAD LUAD ESCA
do
python bin/feature-selction.py --input ~/Documents/bioinfo/pico-analysis/variations/expression/matrix/siqi-filter.TMM.txt \
--log log/${cancer}-no_${cancer}-${selector}-${classifier}.txt \
--feature selected-features/${cancer}-no_${cancer}-${selector}.txt \
--pos_ids ~/Documents/bioinfo/pico-analysis/sample_ids/strigent-filter/${cancer}.txt  \
--neg_ids ~/Documents/bioinfo/pico-analysis/sample_ids/strigent-filter/no-${cancer}.txt
done
done
done
