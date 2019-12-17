import pandas as pd
import argparse
import sys

parser = argparse.ArgumentParser(description='Filter Matrix by Expression or NaN values')
parser.add_argument('--input', '-i', type=str, required=True, help='input matrix')
parser.add_argument('--method','-m',type=str,default="by_na",choices=["by_na","by_value"])
parser.add_argument('--threshold','-s',type=float,help="threshold for a gene to be condidered as expressed",default=None)
parser.add_argument('--proportion','-p',type=float,default=0.2,help="More than p of the samples should satistify this condition")
parser.add_argument('--stratify','-st',default=None,help="input table for filter stratification")
parser.add_argument('--stratify_key','-sk',help="stratifiy according to which column in input table")
parser.add_argument('--collapse','-c',choices=["union","intersection"],default="union",help="How to collapse stratified filtered results")
parser.add_argument('--output','-o',type=str,required=True,help='output path')
parser.add_argument('--pass_gene_ids','-ps',type=str,help="where to store gene ids pass filtrations",default=None)
args = parser.parse_args()

if args.method == "by_value":
    if args.threshold is None:
        print("threshold should be specify if filter by value")
        sys.exit(1)
else:
    args.threshold = None

if args.stratify is not None:
    if args.stratify_key is None:
        print("keys should be specified if use stratified filter")



def filtration(df,p,condition=None):
    n_min = int(df.shape[1]*p)
    if condition is None:
        df = df[(~df.isna()).sum(axis=1)>n_min]
    else:
        df = df[(df>condition).sum(axis=1)>n_min]
    return df



df = pd.read_csv(args.input,sep="\t",index_col=0)
print("Input features : {}".format(df.shape[0]))

if args.stratify is None:
    df_filtered = filtration(df,args.proportion,condition=args.threshold)
else:
    index = set()
    table = pd.read_csv(args.stratify,sep="\t",index_col=0)
    if args.stratify_key not in table.columns:
        print("Stratified Variable not present in the input table")
        sys.exit(1)
    first = True
    for stra in table[args.stratify_key].unique():
        subids = table[table[args.stratify_key]==stra].index
        print("For {} {} samples in input table".format(len(subids),stra))
        subids = set(subids).intersection(df.columns)
        if len(subids) == 0:
            print("No samples exist in matrix, skip .")
            continue
        print("{} are present in the input matrix".format(len(subids)))
        subdf = filtration(df.loc[:,subids],args.proportion,condition=args.threshold)
        print("{} features retained".format(len(subdf.index)))
        if args.collapse == "union" or first:
            index = index.union(set(subdf.index))
        else:
            index = index.intersection(set(subdf.index))
        first = False
    df_filtered = df.loc[index,:]
        
print("Features pass the filtration: {}".format(df_filtered.shape[0]))

print(df_filtered.head())
df_filtered.to_csv(args.output,sep="\t")

if args.pass_gene_ids is not None:
    with open(args.pass_gene_ids,"w") as f:
        f.write("\n".join(df_filtered.index)+"\n")
