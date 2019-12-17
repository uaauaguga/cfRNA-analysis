import pandas as pd
import argparse
import numpy as np
parser = argparse.ArgumentParser(description='Recover ENSG ID/exSeek id with gene length other than merged to exSeek ID')
parser.add_argument('--input', '-i', type=str, required=True, help='input matrix')
parser.add_argument('--output','-o',type=str,required=True,help='output path')
parser.add_argument('--idmapping','-m',type=str,required=True)
args = parser.parse_args()

df = pd.read_csv(args.input,sep="\t",index_col=0)
print("Input shape: ",df.shape[0])
df.index = df.index.map(lambda x:x.split("|")[0].split(".")[0])
df = df[~df.index.duplicated()]
print("After remove duplicated features:",df.shape[0])
mapping = pd.read_csv(args.idmapping,sep="\t",index_col=0)
mapping = mapping[~mapping.index.duplicated()]
commonId = np.intersect1d(df.index,mapping.index)
print("After remove ID not present in the length table: ",commonId.shape[0])
df = df.loc[commonId,:]
df.index = mapping.loc[commonId,"longId"]
df.to_csv(args.output,sep="\t")
