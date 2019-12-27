import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import argparse
import sys
parser = argparse.ArgumentParser(description='Plot RLE')
parser.add_argument('--input', '-i', type=str, required=True, help='input count matrix')
parser.add_argument('--covariates','-c',type=str,required=True,help='covariates')
parser.add_argument('--key','-k',type=str,required=True,help='keys used in covariates table')
parser.add_argument('--output','-o',type=str,required=True,help='RLE pdf path')
args = parser.parse_args()


path = args.input
mat = pd.read_csv(path,sep="\t",index_col=0)
key = args.key
covariates = pd.read_csv(args.covariates,index_col=0,sep="\t")
sample_ids = np.intersect1d(mat.columns,covariates.index)
mat = mat.loc[:,sample_ids]
covariates = covariates.loc[sample_ids,:]
batch = covariates[key].sort_values()
pseudoCount = 1
logMat = np.log(mat+pseudoCount)
rleMat = logMat - logMat.median(axis=1).values.reshape((-1,1))
fig,ax = plt.subplots(figsize=(10,7))
flierprops = dict(marker='o', markersize=0.5,
                  linestyle='none', markeredgecolor='g')
c = "red"
p = ax.boxplot(rleMat.loc[:,batch.index].T,flierprops=flierprops,patch_artist=True)
colors = pd.Series(plt.get_cmap("Dark2").colors)
currentBatch = ""
i = -1
s = 0
for sample_id in batch.index:
    if batch.loc[sample_id] != currentBatch:
        currentBatch = batch.loc[sample_id]
        i += 1
    color = colors.iloc[i]
    p["boxes"][s].set(color = color )
    s += 1


ticks = []
tmp = pd.DataFrame(np.unique(batch,return_counts=True)).T.set_index(0)
tmp.columns = ["number"]
pos = (tmp.cumsum()-tmp/2).astype(int)
pos = pos.loc[tmp[tmp["number"]>2].index]
for i in range(len(sample_ids)):
    cur = None
    for j,bat in enumerate(pos["number"]):
        if i == bat:
            cur = pos.index[j]
            break
    if cur is not None:
        ticks.append(cur)
    else:
        ticks.append("")

ax.tick_params(length=0)
plt.xticks(range(len(ticks)),ticks,rotation='vertical')

plt.savefig(args.output)
