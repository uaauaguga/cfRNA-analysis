from scipy.stats import ranksums
import pandas as pd
import numpy as np
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description="perform Ranksum Test...")
parser.add_argument("--input","-i",help="input matrix")
parser.add_argument("--coverage","-c",help="path of coverage file",default=None)
parser.add_argument("--method","-m",help="by position or by gene",default="byposition",choices=["bygene","byposition"])
parser.add_argument("--output","-o",help="path for output")
parser.add_argument("--pos_ids","-p",help="positive sample ids")
parser.add_argument("--neg_ids","-n",help="negative sample ids")
parser.add_argument("--mincov","-mc",help="minimal coverage for each position",default=3)
parser.add_argument("--minsample","-ms",help="minmal samples for differential editing analysis",default=3)
args = parser.parse_args()
coverage = args.coverage

method = args.method
if method=="byposition":
    mincov = args.mincov
elif method=="bygene":
    mincov = 0

minsample = args.minsample


from statsmodels.stats.multitest import multipletests

def rankSumTest(ser,pos,neg):
    return ranksums(ser.loc[pos],ser.loc[neg]).pvalue

def check(cov,pos,neg):
    global mincov
    pos_cov = cov.loc[pos].fillna(0)
    neg_cov = cov.loc[neg].fillna(0)
    pos_ids = pos_cov[pos_cov>mincov].index
    neg_ids = neg_cov[neg_cov>mincov].index
    return pos_ids,neg_ids

def test(df,pos_ids,neg_ids):
    records = []
    global method
    global coverage
    global minsample
    used = 0
    unused = 0
    if method=="byposition":
        coverageDf = pd.read_table(coverage,index_col=0)
    else:
        coverageDf = df
    print("Caculate p vlaues ...")
    for index in tqdm(df.index):
        cov = coverageDf.loc[index,:]
        pos,neg = check(cov,pos_ids,neg_ids)
        if len(pos)< minsample or len(neg) < minsample:
            unused += 1
            continue
        used += 1
        pvalue = rankSumTest(df.loc[index,:],pos,neg)
        diff = df.loc[index,pos_ids].mean()-df.loc[index,neg_ids].mean()
        records.append((index,pvalue,diff))
    res = pd.DataFrame.from_records(records)
    res.columns = ["index","p","diff"]
    res = res.set_index("index")
    print("{} sites are tested, {} sites are filtered".format(used,unused))
    print("Adjust FDR ...")
    res["padj"] = multipletests(res["p"],method="fdr_bh")[1]
    print("Done .")
    return res


matrixPath = args.input
pos_ids = open(args.pos_ids).read().strip().split("\n")
neg_ids = open(args.neg_ids).read().strip().split("\n")
df = pd.read_table(matrixPath,index_col=0)
print("Among the input {} positive samples, {} negative samples".format(len(pos_ids),len(neg_ids)))
pos_ids = set(pos_ids).intersection(set(df.columns))
neg_ids = set(neg_ids).intersection(set(df.columns))
print("{} postive samples and {} negative samples are finally used".format(len(pos_ids),len(neg_ids)))
res = test(df,pos_ids,neg_ids) 
res.to_csv(args.output,sep="\t")


