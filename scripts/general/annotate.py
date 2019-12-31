import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Summarize Number of RNA type for diff analysis results")
parser.add_argument('-i','--input',help='Input boolean coded matrix',required=True)
parser.add_argument('-k','--key',help='which field in the index to use',default=1,type=int)
parser.add_argument('-o','--output',help='Count matrix group by RNA types, etc',required=True)
args = parser.parse_args()

df = pd.read_csv(args.input,sep="\t",index_col=0)
df["RNA-type"] = df.index.map(lambda x:x.split("|")[args.key])   
dfGrouped = df.groupby("RNA-type").sum(axis=0)
dfGrouped.to_csv(args.output,sep="\t")   
     
