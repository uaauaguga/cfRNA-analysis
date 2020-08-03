import os
import pandas as pd
import numpy as np
from tqdm import tqdm
#df.columns = ["edit-ID","sample_id","n-support","n-edit"]
print("Load data ...")
df = pd.read_csv("editing-level/coverage-summary-by-position.txt",sep="\t")
print("Done .")
print("Pivot axis ...")
coverage = df.pivot(index="edit-ID",columns="sample_id",values="n-support")
editing = df.pivot(index="edit-ID",columns="sample_id",values="n-edit")
print("Done .")
print("Write editing level by position ...")
coverage.to_csv("editing-level/coverage-by-pos.txt",sep="\t")
editing.to_csv("editing-level/editing-by-pos.txt",sep="\t")
print("Done .")
print("Collapse signal by gene ...")
pos2gene = pd.read_csv("recurrent-sites/pos2gene.txt",sep="\t")
pos2gene.columns = ["pos","gene"]
geneCoverage = pos2gene.groupby("gene").apply(lambda x:coverage.loc[np.intersect1d(x["pos"].values,coverage.index),:].sum(axis=0))
geneEditing = pos2gene.groupby("gene").apply(lambda x:editing.loc[np.intersect1d(x["pos"].values,editing.index),:].sum(axis=0))
print("Done .")
print("Write editing level by gene ...")
geneCoverage.to_csv("editing-level/coverage-by-gene.txt",sep="\t")
geneEditing.to_csv("editing-level/editing-by-gene.txt",sep="\t")
print("Done")
