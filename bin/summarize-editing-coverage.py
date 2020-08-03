import os
import pandas as pd
import numpy as np
from tqdm import tqdm
#chrom pos ref  n_ref  n_edit  depth
records = []
for i in tqdm(os.listdir("coverage")):
    sample_id = i.split(".")[0]
    with open("coverage/{}.txt".format(sample_id)) as f:
        for i,line in enumerate(f):
            if i==0:
                continue
            chrom,pos,ref,n_ref,n_edit,depth = line.strip().split("\t")
            n_ref = int(n_ref)
            n_edit = int(n_edit)
            editId = chrom + "|" + pos
            records.append((editId,sample_id,n_ref+n_edit,n_edit))
df = pd.DataFrame.from_records(records)
df.columns = ["edit-ID","sample_id","n-support","n-edit"]
df.to_csv("editing-level/coverage-summary-by-position.txt",sep="\t",index=False)
            
