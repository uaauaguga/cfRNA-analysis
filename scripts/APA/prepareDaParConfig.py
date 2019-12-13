import argparse
import pandas as pd
import numpy as np
parser = argparse.ArgumentParser(description='Prepare Configuration File for DaPar')
parser.add_argument('--dataset', '-d', type=str, required=True, help='dataset')
parser.add_argument('--pos','-p',type=str,required=True,help='Positive class')
parser.add_argument('--neg','-n',type=str,required=True,help='Negative class')
parser.add_argument('--output','-o',type=str,required=True,help="Where to put the configuration file")
parser.add_argument('--coverage','-c',type=str,default="30",help="Minimal coverage")
args = parser.parse_args()

dataset = args.dataset
coverage = args.coverage
pos = args.pos
neg = args.neg

sampleClasses = pd.read_csv("data/{}/sample_classes.txt".format(dataset),index_col=0,sep="\t")
posIds = sampleClasses.index[np.where(sampleClasses.iloc[:,0]==args.pos)]
negIds = sampleClasses.index[np.where(sampleClasses.iloc[:,0]==args.neg)]

posWigs=[ "output/{}/wig_merged/{}.wig".format(dataset,sample_id) for sample_id in posIds]
negWigs=[ "output/{}/wig_merged/{}.wig".format(dataset,sample_id) for sample_id in negIds]

posWigStr = ",".join(posWigs)
negWigStr = ",".join(negWigs)
outDir = "output/{}/APA/{}-{}".format(dataset,pos,neg)
outFile = "{}-{}.dapar.txt".format(pos,neg)

template="""Annotated_3UTR=long_RNA_3_UTR.bed
Group1_Tophat_aligned_Wig={}
Group2_Tophat_aligned_Wig={}
Output_directory={}
Output_result_file={}
Num_least_in_group1=1
Num_least_in_group2=1
Coverage_cutoff={}
FDR_cutoff=0.05
PDUI_cutoff=0.5
Fold_change_cutoff=0.59"""

with open(args.output,"w") as f:
    f.write(template.format(posWigStr,negWigStr,outDir,outFile,coverage))
