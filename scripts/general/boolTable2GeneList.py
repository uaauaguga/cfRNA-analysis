import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Prepare Gene List fils from bool matrix")
parser.add_argument("--input","-i",help="Input bool matrix")
parser.add_argument("--outdir","-o",help="Dir for output")
args = parser.parse_args()

mat = pd.read_csv(args.input,sep="\t",index_col=0)

for each in mat.columns:
    print(each)
    genes = mat[mat[each]==1].index.map(lambda x:x.split(".")[0]).to_list()
    out = "\n".join(genes)
    with open(args.outdir+"/"+each+".txt","w") as f:
        f.write(out+"\n")
