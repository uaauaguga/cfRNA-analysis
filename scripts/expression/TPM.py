import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import pandas as pd
import argparse
import sys
parser = argparse.ArgumentParser(description='Calculate TPM')
parser.add_argument('--input', '-i', type=str, required=True, help='input count matrix')
parser.add_argument('--output','-o',type=str,required=True,help='output TPM matrix')
parser.add_argument('--length','-l',type=str,default="/home/jinyunfan/Documents/bioinfo/pico-analysis/gene-length/gene-length.txt",help='gene length table')
args = parser.parse_args()
df = pd.read_csv(args.input,index_col=0,sep="\t")
length_df = pd.read_csv(args.length,index_col=0,sep="\t")
length_df.index = length_df.index.map(lambda x:x.split(".")[0])
df.index = df.index.map(lambda x:x.split("|")[0].split('.')[0])
df = df.loc[~df.index.duplicated(keep='first')]
length_df = length_df.loc[~length_df.index.duplicated(keep='first')]
commongene = set(df.index).intersection(set(length_df.index))
print(len(df.index)," input genes")
print(len(commongene)," are utilized")
df = df.loc[commongene,:]
length_df = length_df.loc[commongene,:]
lengthScaledDf = pd.DataFrame((df.values/length_df.values),index=commongene,columns=df.columns)
(1000000*lengthScaledDf.div(lengthScaledDf.sum(axis=0))).round(4).to_csv(args.output,sep="\t")

