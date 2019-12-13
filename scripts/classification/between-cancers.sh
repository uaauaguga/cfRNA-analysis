#!/bin/bash
selector=ranksum
classifier=RF
for cancer in CRC STAD LUAD ESCA #HCC
do
python bin/feature-selction.py --input ~/Documents/bioinfo/pico-analysis/variations/expression/matrix/siqi-filter.TMM.txt \
--log between-cancers/log-${cancer}-no_${cancer}-${selector}-${classifier}.txt \
--feature between-cancers/selected-features-${cancer}-no_${cancer}-${selector}.txt \
--pos_ids ~/Documents/bioinfo/pico-analysis/sample_ids/discovery-set/${cancer}.txt  \
--neg_ids ~/Documents/bioinfo/pico-analysis/sample_ids/discovery-set/no-${cancer}.txt \
--number 300
done
