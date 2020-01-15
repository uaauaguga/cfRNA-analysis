import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Summarize Number of RNA type for diff analysis results")
parser.add_argument('-i','--input',help='Input count matrix',required=True)
parser.add_argument('-s','--threshold',type=float,help='Threshold for one gene to be considered as expressed',default=2)
parser.add_argument('-o','--output',help='Count matrix group by RNA types, etc',required=True)
args = parser.parse_args()


def stat(path,threshold):
    df = pd.read_csv(path,sep="\t",index_col=0)
    df["type"] = df.index.map(lambda x:x.split("|")[1])
    return df.groupby("type").apply(lambda x:(x>threshold).sum(axis=0))


res = stat(args.input,args.threshold)

res.to_csv(args.output,sep="\t")
