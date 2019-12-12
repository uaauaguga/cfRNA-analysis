import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Summarize Number of RNA type for diff analysis results")
parser.add_argument('-i','--input',help='Input boolean coded matrix',required=True)
parser.add_argument('-o','--output',help='Count matrix group by RNA types, etc',required=True)
parser.add_argument('-t','--transcript_table',help='Transcript table',required=True)
args = parser.parse_args()

df = pd.read_csv(args.input,sep="\t",index_col=0)
table = pd.read_csv(args.transcript_table,sep="\t")


table = table.loc[:,["gene_id","gene_type"]]
table["gene_id"] = table["gene_id"].map(lambda x:x.split(".")[0])
table = table.drop_duplicates(subset="gene_id").set_index("gene_id")

df.index = df.index.map(lambda x:x.split("|")[0].split(".")[0])
used_ids = set(table.index).intersection(set(df.index))
n_used = len(used_ids)
n_unused = len(df.index) - n_used
   
print("Among {} genes,".format(len(df.index))) 
print("{} genes are annotated, {} genes are not annotated".format(n_used,n_unused))


df = df.loc[used_ids,:]
df["RNAType"] = table.loc[used_ids,:]       
dfGrouped = df.groupby("RNAType").sum(axis=0)
dfGrouped.to_csv(args.output,sep="\t")   
     
