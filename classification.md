## Normalization / removing unwanted variations for gene expression counts and metagenomics counts
```{bash}
## counts: input count matrix
## classes: metadata
## tmm: output tmm normalized data
## ruv: output ruvg normalized data
## anova: output anova statistics table
Rscript bin/normalization.R --counts ${input} --classes metadata/sample_classes.txt --tmm ${tmm} --ruv ${ruv} --anova ${anova}
```

## Evaluation of feature selection methods and classifiers
- Evaluate the stability of feature selection
```{bash}
python bin/FS.py --input ${input} --pos metadata/CRC-dis.txt  --neg metadata/NC-dis.txt --resampling 100 --recurrency 1 --method ${method} --features stability/${method}.txt
```
- Evaluate the performance of feature selection
```{bash}
## Selector: ranksum RF SURF LR-L1  MI random ranksum-SURF 
## Classifier: RF-balanced LR KNN DT SVM
python bin/test-classification.py  --input ${input} --pos CRC --neg NC --selector ${selector} --classifier ${clf} --auroc performance/${selector}:${clf}.txt --labels ${labels} 
```

## Binary feature selection and classification
```
# Cancer vs. HD classification
# see bin/run-variation-cancer-NC.sh and bin/run-expression-cancer-NC.sh
 
# One vs. rest classification for different cancers
# see bin/run-OvR5.sh

# Combine selected features by mixing features and logistic regression
# see bin/get-probability.sh and bin/probability-integration.py 
```

## Multiclass classification
- See bin/multi-class.py 
