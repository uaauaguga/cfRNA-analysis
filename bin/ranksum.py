from scipy.stats import ranksums
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Perform Ranksum Test...")
parser.add_argument("--input","-i",help="Input matrix")
parser.add_argument("--output","-o",help="path for output")
parser.add_argument("--pos_ids","-p",help="positive sample ids")
parser.add_argument("--neg_ids","-n",help="negative sample ids")
parser.add_argument("--diff_method","-m",default="diff",help="diff/log2fc")
args = parser.parse_args()

method = args.diff_method

from statsmodels.stats.multitest import multipletests

def rankSumTest(ser,pos,neg):
    return ranksums(ser.loc[pos],ser.loc[neg]).pvalue

def test(df,pos_ids,neg_ids):
    global method
    res = pd.DataFrame(index=df.index,columns=["p","padj","diff"])
    print("Caculate p vlaues ...")
    res["p"] = df.apply(lambda row:rankSumTest(row,pos_ids,neg_ids),axis=1)
    print("Done .")
    if method=="diff":
        res["diff"] = df.loc[:,pos_ids].mean(axis=1)-df.loc[:,neg_ids].mean(axis=1)
    elif method=="log2fc":
        res["log2fc"] = np.log2(df.loc[:,pos_ids].mean(axis=1))-np.log2(df.loc[:,neg_ids].mean(axis=1))
    print("Adjust FDR ...")
    res["padj"] = multipletests(res["p"],method="fdr_bh")[1]
    print("Done .")
    return res


matrixPath = args.input
pos_ids = open(args.pos_ids).read().strip().split("\n")
neg_ids = open(args.neg_ids).read().strip().split("\n")
df = pd.read_csv(matrixPath,index_col=0)
print("Among the input {} positive samples, {} negative samples".format(len(pos_ids),len(neg_ids)))
pos_ids = set(pos_ids).intersection(set(df.columns))
neg_ids = set(neg_ids).intersection(set(df.columns))
print("{} postive samples and {} negative samples are finally used".format(len(pos_ids),len(neg_ids)))
res = test(df,pos_ids,neg_ids) 
res.to_csv(args.output,sep="\t")
