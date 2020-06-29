import os
import argparse
import pandas as pd


parser = argparse.ArgumentParser(description="Feature Selection")
parser.add_argument("--indir","-i",help="Input Dir, require all matrix in this dir have same columns",required=True)
parser.add_argument("--output","-o",help="label of the s",required=True)
args = parser.parse_args()

dfs = []

cols = None
for matPath in os.listdir(args.indir):
    print("Load {} ...".format(matPath))
    df = pd.read_csv(args.indir + "/" + matPath,sep="\t",index_col=0)
    if cols is None:
        cols = df.columns
    else:
        df = df.loc[:,cols]
    dfs.append(df)

merged = pd.concat(dfs)
merged.to_csv(args.output,sep="\t")
    
    
