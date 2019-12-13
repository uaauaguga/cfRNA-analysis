import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description='Summarize SNP Results')
parser.add_argument('--indir', '-i', type=str, required=True, help='input dir')
parser.add_argument('--muttable','-m',type=str,required=True,help='output mutation table path')
parser.add_argument('--freqtable','-f',type=str,required=True,help='output frequency table path')
parser.add_argument('--odds_ratio','-or',type=str,required=True,help='output odds ratio path')
parser.add_argument('--covariates','-cov',type=str,required=True,help="covariates table")
args = parser.parse_args()


def stat(df):
    """
    For a mutation
    Calculate odds in each class
    If all of the samples in a class has this mutation, suppose an additional sample do not has the mutation
    If none of the samples in a class has this mutation, suppose an additional sample has the mutation
    """
    states = df["state"].unique()
    number = df["number"].unique()[0]
    df = df.set_index("state")
    cancers = ["CRC","ESCA","STAD","LUAD","HCC","Health"]
    res = pd.Series(index=cancers)
    for cancer in cancers:
        if cancer in states:
            frequency = df.loc[cancer,"frequency"]
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



#Load results to one file
mutationRecords = []
#G|A,T|C
print("Prepare mutation table, exclude editing-like conversion ...")
for file in tqdm(os.listdir(args.indir)):
    sample_id = file.split(".")[0]
    df = pd.read_csv(args.indir.strip()+"/"+file,sep="\t",header=None)
    watchDog = set()
    for record in df.to_records():
        if (record[3]=="G" and record[4]=="A") or (record[3]=="T" and record[4]=="C") or (record[3]=="A" and record[4]=="G") or (record[3]=="C" and record[4]=="T"):
            continue
        temp = "|".join((record[1],str(record[2]),record[3],record[4]))
        if temp not in watchDog:
            mutationRecords.append((sample_id,temp))
            watchDog.add(temp)
print("Done .")
print("Write to "+args.muttable+"...")
df = pd.DataFrame.from_records(mutationRecords)
df.columns = ["sample_id","mutation"]
df.to_csv(args.muttable,sep="\t",index=False)
print("Done .")


#Group by disease

print("Summarize mutation frequence in each disease ...")
covariates = pd.read_csv(args.covariates,index_col=0,sep="\t")

print("Among {} samples provided in the input dir".format(df["sample_id"].unique().shape[0]))
common_sample = np.intersect1d(covariates.index,df["sample_id"].unique())
print("{} samples are in the covariates table".format(common_sample.shape[0]))
if common_sample.shape[0] < df["sample_id"].unique().shape[0]:
    print("Some of the samples are not provided in the covariates table, exit")
    sys.exit(1)

df["state"] = covariates.loc[df["sample_id"].values,"Disease"].values
states = df["state"].unique()
records = []
for state in tqdm(states):
    subDf = df[df["state"]==state]
    n = subDf["sample_id"].unique().shape[0]
    countsDf = pd.DataFrame(np.unique(subDf["mutation"],return_counts=True)).T
    countsDf = countsDf.set_index(0)
    countsDf.index.name = "mutation"
    countsDf.columns = ["counts"]
    for mutation,frequency in countsDf.to_records():
        records.append((mutation,frequency,state,n))

frequencyTable = pd.DataFrame.from_records(records)
frequencyTable.columns = ["mutation","frequency","state","number"]
print("Done .")
print("Write to "+args.freqtable+"...")
frequencyTable["ratio"] = frequencyTable["frequency"]/frequencyTable["number"] 
frequencyTable.to_csv(args.freqtable,sep="\t",index=False)
print("Done .")


print("Calculate odds ratio ...")
temp = frequencyTable.groupby("mutation").apply(stat)
print("Done .")
cancers = ["CRC","HCC","STAD","LUAD","ESCA"]
odds = pd.DataFrame(index=temp.index,columns=cancers)

for cancer in cancers:
    print(cancer)
    odds.loc[odds.index,cancer] = (temp[cancer]/temp["Health"])

odds.to_csv(args.odds_ratio,sep="\t")
