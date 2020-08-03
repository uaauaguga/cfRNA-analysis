import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import pandas as pd
import argparse
import sys
parser = argparse.ArgumentParser(description='Merge Two Matrix')
parser.add_argument('--matrix1', '-m1', type=str, required=True, help='the first matrix')
parser.add_argument('--matrix2','-m2',type=str,required=True,help='the second matrix')
parser.add_argument('--output','-o',type=str,required=True,help='output path')
parser.add_argument('--fill','-f',action="store_true",default=True)
args = parser.parse_args()
df1 = pd.read_table(args.matrix1,index_col=0)
df2 = pd.read_table(args.matrix2,index_col=0)
print("Shape of the first input matrix")
print(df1.shape)
print("Shape of the second input matrix")
print(df2.shape)
print("Index in common:")
print(len(set(df1.index).intersection(df2.index)))
mat = df1.join(df2,how='outer')
if args.fill:
    mat = mat.fillna(0)
mat.to_csv(args.output,sep="\t")
