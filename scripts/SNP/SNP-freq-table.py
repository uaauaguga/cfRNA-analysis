import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description='Summarize chimeric RNA Results')
parser.add_argument('--indir', '-i', type=str, required=True, help='input dir contain all results, *abridged.tsv')
parser.add_argument('--sample_ids','-s',type=str,required=True,help='input sample ids')
parser.add_argument('--output','-o',type=str,required=True,help='output frequency table path')
args = parser.parse_args()

print("Summarize results of queried samples into a single file")
records = []
sample_ids = open(args.sample_ids).read().strip().split("\n")
print("Among {} queried samples".format(len(sample_ids)))
all_ids = [each.split(".")[0] for each in os.listdir(args.indir)]
print(np.setdiff1d(sample_ids,all_ids))
sample_ids = np.intersect1d(sample_ids,all_ids)
print("{} are in the provided dir".format(len(sample_ids)))
n_samples = len(sample_ids)

#Load results to one file
mutationRecords = []
#G|A,T|C
print("Prepare mutation table, exclude editing-like conversion ...")
for sample_id in tqdm(sample_ids):
    df = pd.read_csv(args.indir.strip()+"/"+sample_id+".txt",sep="\t",header=None)
    watchDog = set()
    for record in df.to_records():
        if (record[3]=="G" and record[4]=="A") or (record[3]=="T" and record[4]=="C") or (record[3]=="A" and record[4]=="G") or (record[3]=="C" and record[4]=="T"):
            continue
        temp = "|".join((record[1],str(record[2]),record[3],record[4]))
        if temp not in watchDog:
            mutationRecords.append((sample_id,temp))
            watchDog.add(temp)
print("Done .")

df = pd.DataFrame.from_records(mutationRecords)
df.columns = ["sample_id","mutation"]

n = df["sample_id"].unique().shape[0]
freq_table = pd.DataFrame(np.unique(df["mutation"],return_counts=True)).T
freq_table = freq_table.set_index(0)
freq_table.index.name = "mutation"
freq_table.columns = ["n_detected"]
freq_table["n_undetected"] = n_samples - freq_table["n_detected"]
freq_table.to_csv(args.output,sep="\t")

