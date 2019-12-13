import numpy as np
import pandas as pd
import argparse
import HTSeq
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input',help='VCF file from which to extract editing sites',required=True)
parser.add_argument('-d','--editing_db',help="REDIPortal in vcf format",required=True)
parser.add_argument('-a','--annotated',help='Path fo out put of annotated editing sites',required=True)
parser.add_argument('-n','--novel',help="Path for output of novel editing sites",required=True)

args = parser.parse_args()

queryPath = args.input
dbPath = args.editing_db
outAnnotatedPath = args.annotated
outNovelPath = args.novel


db = HTSeq.VCF_Reader(dbPath)
querys = HTSeq.VCF_Reader(queryPath)

annotatedEditingSitesSet = set()
base2index = {"A":0,"C":1,"G":2,"T":3}
print("Load Annotated Sites ... ")
for variant in tqdm(db):
    annotatedEditingSitesSet.add(variant.pos)
print("Done . ")
annotatedQuerys = []
novelQuerys = []
print("Processing querys ...")
for variant in tqdm(querys):
    pos = variant.pos
    metadata = {}
    for record in variant.info.strip().split(";"):
        if len(record)==0:
            continue
        key,value = record.split("=")
        metadata[key] = value
    bases = metadata['BaseCounts'].split(",")
    n_editied = int(bases[base2index[variant.alt[0]]])
    n_uneditied = int(bases[base2index[variant.ref]])
    ratio = n_editied/(n_editied+n_uneditied)
    out = (pos.chrom,pos.start,ratio,n_editied,n_uneditied)
    if variant.pos in annotatedEditingSitesSet:
        annotatedQuerys.append(out)
    else:
        novelQuerys.append(out)
print("Done .")
print("Write to output ...")
annotatedDf = pd.DataFrame(annotatedQuerys,columns=["chrom","1_based_pos","ratio","n_edit","n_ref"])
novelDf = pd.DataFrame(novelQuerys,columns=["chrom","1_based_pos","ratio","n_edit","n_ref"])
annotatedDf.to_csv(outAnnotatedPath,sep="\t",index=False)
novelDf.to_csv(outNovelPath,sep="\t",index=False)
print("Done .")
