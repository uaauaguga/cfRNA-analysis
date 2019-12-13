python bin/feature-selction-v2.py --input ~/Documents/bioinfo/pico-analysis/variations/expression/matrix/siqi-filter.TMM.txt \
	--log test-log.txt \
	--feature test-features.txt \
	--pos_ids ~/Documents/bioinfo/pico-analysis/sample_ids/strigent-filter/STAD.txt  \
	--neg_ids ~/Documents/bioinfo/pico-analysis/sample_ids/strigent-filter/no-STAD.txt \
	--selector ranksum \
	--bagging
