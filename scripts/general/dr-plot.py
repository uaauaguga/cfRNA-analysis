import numpy as np
import pandas as pd
import argparse
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import sys
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description='Dimensional Reduction plot')
parser.add_argument('--input', '-i', type=str, required=True, help='count matrix')
parser.add_argument('--covariates','-c',type=str,required=True,help='covariates table')
parser.add_argument('--key1','-k1',type=str,required=True,help='first key in covariate table for labeling samples')
parser.add_argument('--key2','-k2',type=str,required=False,help='senond key in covariate table for labeling samples')
parser.add_argument('--output','-o',type=str,required=True,help='output path')
parser.add_argument('--genes','-g',type=str,default=None,help='gene ids')
parser.add_argument('--method','-m',type=str,default="PCA",choices=["PCA","TSNA"])
args = parser.parse_args()

mat = pd.read_csv(args.input,sep="\t",index_col=0)
covariates = pd.read_csv(args.covariates,index_col=0,sep="\t")

if args.genes is not None:
    features = open(args.genes).read().strip().split("\n")
else:
    features = mat.index

print("Samples provided in covariates table: {}".format(covariates.shape[0]))
print("Samples provided in expression matrix: {}".format(mat.shape[1]))
sample_ids = set(mat.columns).intersection(set(covariates.index))
print("Samples present in both matrix: {}".format(len(sample_ids)))


X = StandardScaler().fit_transform(mat.loc[features,sample_ids].T)

if args.method == "PCA":
    transformer = PCA(n_components=2)
elif args.method == "TSNE":
    transformer = TSNE()

print("Perform dimensional reduction with {} .. ".format(args.method))
mat2d = transformer.fit_transform(X) 
print("Done .")
covariates = covariates.loc[sample_ids,:]
covariates["dim-1"] = mat2d[:,0]
covariates["dim-2"] = mat2d[:,1]

fig,ax = plt.subplots(figsize=(7,7))

if args.key1 not in covariates.columns:
    print("The first key should present in the covariates table")
    sys.exit(1)
elif args.key2 is not None and args.key2 not in covariates.columns:
    print("The second key should present in the covariates table")
    sys.exit(1)

print("Plot figure ..")
sns.scatterplot(data=covariates,x="dim-1",y="dim-2",hue=args.key1,style=args.key2)

if args.method == "PCA":
    ax.set_xlabel("PCA-1")
    ax.set_ylabel("PCA-2")
elif args.method == "TSNE":
    ax.set_xlabel("TSNE-1")
    ax.set_ylabel("TSNE-2")

plt.savefig(args.output)
print("Done ..")
