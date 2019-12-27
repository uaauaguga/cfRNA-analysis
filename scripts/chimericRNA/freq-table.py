import pandas as pd
import numpy as np
import os
import argparse
from tqdm import tqdm


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
for sample_id in sample_ids:
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
results.columns = ["sample_id","fusion-gene"]


records = []
n_samples = len(sample_ids)
freq_table = pd.DataFrame(np.unique(results["fusion-gene"],return_counts=True)).T
freq_table= freq_table.set_index(0)
freq_table.index.name = "fusion-gene"
freq_table.columns = ["n_detected"]
freq_table["n_undetected"] = n_samples - freq_table["n_detected"]
freq_table.to_csv(args.output,sep="\t")
