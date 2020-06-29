import os
import argparse
import pandas as pd
import numpy as np
from scipy.stats import pearsonr,ranksums

parser = argparse.ArgumentParser(description="Identify gender unrelated features")
parser.add_argument("--input","-i",help="Input matrix",required=True)
parser.add_argument("--whitelist","-w",help="Output white list",required=True)
parser.add_argument("--metadata","-m",help="Age and sex should be provided",required=True)
args = parser.parse_args()


def getCorr(x,age):
    r,p = pearsonr(x.values,age.astype(int).values)
    return pd.Series(index=["r","p"],data=[r,p])


def rankSum(x,pos_ids,neg_ids):
    _,p  = ranksums(x.loc[pos_ids].values,x.loc[neg_ids].values)
    log2FC = np.log2(x.loc[pos_ids].mean()/x.loc[neg_ids].mean())
    return pd.Series(data=[log2FC,p],index=["log2FC","p"])

print("Load matrix and metadata ...")
df = pd.read_csv(args.input,sep="\t",index_col=0).fillna(0) 
metadata = pd.read_csv(args.metadata,sep="\t",index_col=0)
metadata = metadata[~(metadata["Age"]=="U")]
df = df.loc[:,metadata.index]
print("Done .")

print("Identify gender related gene ...")
pos_ids = metadata[metadata["gender"]=="M"].index
neg_ids = metadata[metadata["gender"]=="F"].index
genderDiff = df.apply(lambda x:rankSum(x,pos_ids,neg_ids),axis=1)
genderUnRelated = genderDiff[genderDiff["p"]>0.05].index
print("Done .")

#print("Identify age related gene ...")
#correlation = df.apply(lambda x:getCorr(x,metadata["Age"]),axis=1)
#ageUnRelated = correlation[correlation["p"]>0.05].index
#print("Done ..")

print("Among {} genes".format(df.shape[0]))
#print("{} genes are unrelated to age, {} genes are unrealted to gender".format(ageUnRelated.shape[0],genderUnRelated.shape[0]))
print("{} genes are unrealted to gender".format(genderUnRelated.shape[0]))
#whiteList = np.intersect1d(genderUnRelated,ageUnRelated)
whiteList = genderUnRelated
print("{} genes retained".format(whiteList.shape[0]))
with open(args.whitelist,"w") as f:
    f.write("\n".join(list(whiteList)))
