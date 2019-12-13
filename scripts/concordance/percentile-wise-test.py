import pandas as pd
import numpy as np
import argparse
from tqdm import tqdm 

parser = argparse.ArgumentParser(description='Pairwise Perform Hypergeometric Test Between Percentiles')
parser.add_argument('--table1', '-t1', type=str, required=True, help='first de table')
parser.add_argument('--table2','-t2',type=str,required=True,help='second de table')
parser.add_argument('--label1','-l1',type=str,required=True,help='first label')
parser.add_argument('--label2','-l2',type=str,required=True,help="second label")
parser.add_argument('--output','-o',type=str,required=True,help='output pdf path')
args = parser.parse_args()


from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import hypergeom

def loadData(path):
    df = pd.read_csv(path,sep="\t",index_col=0)
    df.index = df.index.map(lambda x:x.split(".")[0])
    df = df[~df.index.duplicated()]
    return df["log2FoldChange"]#*(-np.log10(df["pvalue"]))

rank1 = loadData(args.table1)
rank2 = loadData(args.table2)
index = list(np.intersect1d(rank1.index,rank2.index))
rank1 = rank1.loc[index].sort_values(ascending=False)
rank2 = rank2.loc[index].sort_values(ascending=False)
step = int(rank1.shape[0]/10)
                
RRHO = np.ones((int(rank1.shape[0]/step)+1,int(rank1.shape[0]/step)+1))
for i,step_i in tqdm(enumerate(np.arange(0,rank1.shape[0],step))):
    for j,step_j in enumerate(np.arange(0,rank2.shape[0],step)):
        k = np.intersect1d(rank1.index[step_i:step_i+step],rank2.index[step_j:step_j+step]).shape[0]
        RRHO[i,j] = 1-hypergeom(M=rank1.shape[0],n=step,N=step).cdf(k)

fig,ax = plt.subplots(figsize=(6,6))
im = ax.matshow(-np.log10(RRHO[:-1,:-1]+1e-16).T[::-1])
fig.colorbar(im)
ax.tick_params(axis="x", bottom=True, top=False, labeltop=False,labelbottom=True)
ax.set_xticklabels(np.arange(10,110,10))
ax.set_xticks(np.arange(10))
ax.set_yticklabels(np.arange(100,0,-10))
ax.set_yticks(np.arange(10))
                                            
ax.set_xlabel("{}-percentiles".format(args.label1))
ax.set_ylabel("{}-percentiles".format(args.label2))
ax.set_title("{}:{}".format(args.label1,args.label2))
plt.savefig(args.output)
