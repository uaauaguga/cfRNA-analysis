import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import pandas as pd
import argparse
import sys
parser = argparse.ArgumentParser(description='Extract certain columns from a large matrix')
parser.add_argument('--input', '-i', type=str, required=True, help='the first matrix')
parser.add_argument('--output','-o',type=str,required=True,help='output path')
parser.add_argument('--sample_ids','-s',type=str,default=None,help='sample ids')
parser.add_argument('--genes','-g',type=str,default=None,help='gene ids')
args = parser.parse_args()


df = pd.read_table(args.input,index_col=0)
print(df.shape)
if args.sample_ids is not None:
    sample_ids=open(args.sample_ids).read().strip().split("\n")
    sample_ids = set(sample_ids).intersection(set(df.columns))
    sample_ids = list(sample_ids)
    print("Number of selected samples:",len(sample_ids))
    sample_ids = sorted(sample_ids)
else:
    sample_ids = list(df.columns)
if args.genes is not None:
    gene_ids = open(args.genes).read().strip().split("\n")
    gene_ids = set(gene_ids).intersection(set(df.index))
    print("Number of selected genes:",len(gene_ids))
else:
    gene_ids = list(df.index)

mat = df.loc[gene_ids,sample_ids]
mat.to_csv(args.output,sep="\t")
