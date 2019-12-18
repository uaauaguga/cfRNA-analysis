import pandas as pd
import argparse
import sys
import numpy as np
from scipy.stats import spearmanr

parser = argparse.ArgumentParser(description='Overlap Two Defferentially Expressed Table')
parser.add_argument('--table1', '-t1', type=str, required=True, help='the first de table')
parser.add_argument('--table2','-t2',type=str,required=True,help='the second de table')
parser.add_argument('--diff_key','-k',type=str,default="log2FoldChange",help="which columns used")
parser.add_argument('--label1','-l1',type=str,required=True,help='label of first de table')
parser.add_argument('--label2','-l2',type=str,required=True,help='label of second de table')
args = parser.parse_args()

df1 = pd.read_csv(args.table1,sep="\t",index_col=0)
df2 = pd.read_csv(args.table2,sep="\t",index_col=0)

print("{} genes in first table".format(df1.shape[0]))
print("{} genes in second table".format(df2.shape[0]))

common = np.intersect1d(df1.index,df2.index)

print("{} genes in common".format(common.shape[0]),file=sys.stderr)

res = spearmanr(df1.loc[common,args.diff_key].values,df2.loc[common,args.diff_key].values)[0]

print("{}\t{}\t{}".format(args.label1,args.label2,res),sys.stdout)




