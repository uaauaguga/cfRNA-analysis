import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Ranking DE Table")
parser.add_argument("--input","-i",help="Input matrix")
parser.add_argument("--output","-o",help="path for output")
parser.add_argument("--metric","-m",default="pi",choices=["pi","log2fc"],help="gene ranking metric")
parser.add_argument("--topngene","-n",default=20,help="How many genes to select from the detable")
args = parser.parse_args()

def loadData(path):
    df = pd.read_csv(path,sep="\t",index_col=0)
    df["pi"] = df["log2FoldChange"]*(-np.log10(df["pvalue"]))
    return df


data = loadData(args.input)

if args.metric=="pi":
    res = data.loc[:,"pi"].sort_values(ascending=False)
elif args.metric=="log2fc":
    res = data.loc[:,"log2FoldChange"].sort_values(ascending=False)

res=res.to_frame()
res.columns=[args.metric]
res.to_csv(args.output,sep="\t")
