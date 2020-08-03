#!/bin/bash
import os
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
#1	1266985	.	T	C	61.74	.
exclude = []
indir="output/pico-final/RNAEditor"
sample_ids=open("data/pico-final/sample_ids.txt").read().strip().split("\n")
counts = defaultdict(int)
for sample_id in tqdm(sample_ids):
    vcf = indir+"/{}/{}.editingSites.vcf".format(sample_id,sample_id)
    if os.path.exists(vcf):
        f = open(vcf)
        for line in f:
            if line.startswith("#"):
                continue
            data = line.split("\t")
            chrom,pos,ref,alt = data[0],data[1],data[3],data[4]
            editingId = chrom+"|"+pos+"|"+ref+"|"+alt 
            counts[editingId] += 1
res = pd.Series(counts)
res = pd.DataFrame(res)
res.columns = ["counts"]
res.to_csv("editing-recurrence.txt",sep="\t")
