import pandas as pd
import numpy as np
import os
import argparse
from tqdm import tqdm


parser = argparse.ArgumentParser(description='Summarize chimeric RNA Results')
parser.add_argument('--indir', '-i', type=str, required=True, help='input dir contain all results, *abridged.tsv')
parser.add_argument('--chimerictable','-c',type=str,default=None,help='where to put chimeric RNA statistics')
parser.add_argument('--covariates','-cov',type=str,required=True,help='covariates path')
parser.add_argument('--freqtable','-f',type=str,default=None,help='output frequency table path')
parser.add_argument('--venn','-v',type=str,default=None,help='bool matrix for detected chimeric RNA')
parser.add_argument('--odds_ratio','-or',type=str,default=None,help='output odds ratio path')
parser.add_argument('--mincount','-mc',type=int,required=True,help="Minumum frequency for a chimeric RNA to be considered as exist in a group",default=1)
args = parser.parse_args()



def stat(df):
    """
    For a chimeric RNA
    Calculate odds in each class
    If all of the samples in a class has this mutation, suppose an additional sample do not has the mutation
    If none of the samples in a class has this mutation, suppose an additional sample has the mutation
    """
    states = df["state"].unique()
    number = df["n-samples"].unique()[0]
    df = df.set_index("state")
    cancers = ["CRC","ESCA","STAD","LUAD","HCC","Health"]
    res = pd.Series(index=cancers)
    for cancer in cancers:
        if cancer in states:
            frequency = df.loc[cancer,"n-samples"]
            if df.loc[cancer,"ratio"] == 1:
                # all of the samples in a class has this mutation
                ratio = frequency/(frequency+1)
            else:
                ratio = df.loc[cancer,"ratio"]
        else:
            #none of the samples in a class has this mutation
            ratio = 1/(number+1)
        res.loc[cancer] = ratio/(1-ratio)
    return res


print("Summarize results in input dir into a single file")
records = []
covariates = pd.read_csv(args.covariates,index_col=0,sep="\t")
for file in os.listdir(args.indir):
    sample_id = file.split(".")[0]
    if sample_id not in covariates.index:
        continue
    path = args.indir.strip()+"/{}.tsv".format(sample_id)
    df = pd.read_csv(path,sep="\t")
    tmp = set()
    for record in df.loc[:,["LeftGene","RightGene"]].to_records():
        _,left,right = record
        fusion = "{}:{}".format(left,right)
        if fusion in tmp:
            continue
        tmp.add(fusion)
        records.append((sample_id,fusion))

results = pd.DataFrame.from_records(records)
print(results.head())
results.columns = ["sample_id","fusion-gene"]

if args.chimerictable is not None:
    results.to_csv(args.chimerictable,sep="\t")

results["detected"] = 1

results["state"] = covariates.loc[results["sample_id"].values,"Disease"].values

from tqdm import tqdm
cancers = ["CRC","STAD","LUAD","HCC","ESCA","Health"]
records = []
for cancer in tqdm(cancers):
    subDf = results[results["state"]==cancer]
    n = subDf["sample_id"].unique().shape[0]
    subDf = pd.DataFrame(np.unique(subDf["fusion-gene"],return_counts=True)).T
    subDf = subDf.set_index(0)
    subDf.index.name = "fusion-gene"
    subDf.columns = ["counts"]
    for fusion,frequency in subDf.to_records():
        records.append((fusion,frequency,cancer,n))

freqTable = pd.DataFrame.from_records(records)
freqTable.columns = ["fusion-id","counts","state","n-samples"]
freqTableFiltered = freqTable[freqTable["counts"]>args.mincount].copy()
freqTableFiltered["detected"] = 1


if args.freqtable is not None:
    freqTableFiltered.to_csv(args.freqtable,sep="\t",index=False)


if args.venn is not None:
    venn = freqTableFiltered.pivot(index="fusion-id",columns="state",values="detected").fillna(0).astype(int)
    venn.to_csv(args.venn,sep="\t")

freqTableFiltered.loc[:,"ratio"] = freqTableFiltered["counts"]/freqTableFiltered["n-samples"]

if args.odds_ratio is not None:
    temp = freqTableFiltered.groupby("fusion-id").apply(stat)
    cancers = ["CRC","ESCA","STAD","LUAD","HCC"]
    odds = pd.DataFrame(index=temp.index,columns=cancers)
    for cancer in cancers:
        print(cancer)
        odds.loc[odds.index,cancer] = (temp.loc[:,cancer]/temp.loc[:,"Health"])
    odds.to_csv(args.odds_ratio,sep="\t")
