import os
import argparse
import pandas as pd


parser = argparse.ArgumentParser(description="Add trend for selected features")
parser.add_argument("--input","-i",help="RUVg normalized matrix",required=True)
parser.add_argument("--features","-f",help="Input selected features",required=True)
parser.add_argument("--metadata","-m",help="Class label",required=True)
parser.add_argument("--pos","-p",help="Positive class",required=True)
parser.add_argument("--neg","-n",help="Negative class",default="NC")
parser.add_argument("--output","-o",help="Selected features with fold change",required=True)
args = parser.parse_args()


df = pd.read_csv(args.input,sep="\t",index_col=0) 
features = pd.read_csv(args.features,sep="\t",index_col=0)
metadata = pd.read_csv(args.metadata,sep="\t",index_col=0)

pos_ids = metadata[metadata["labels"]==args.pos].index
neg_ids = metadata[metadata["labels"]==args.neg].index

diff = df.loc[features.index,pos_ids].mean(axis=1)-df.loc[features.index,neg_ids].mean(axis=1)

features["diff"] = diff

features.to_csv(args.output,sep="\t")

   
