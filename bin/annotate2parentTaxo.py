import argparse
import pandas as pd
import numpy as np
import os

levels = ["kingdom","phylum","class","order","family","genus","species"]
hierarchy = {}
for i,level in enumerate(levels):
    hierarchy[level] = i
hierarchy = pd.Series(hierarchy)

parser = argparse.ArgumentParser(description="Annotate node in taxo tree to higher classification level")
parser.add_argument("--nodes",help="Input NCBI classification tree nodes",default="nodes.txt")
parser.add_argument("--input","-i",help="Input NCBI taxo id",default=None)
parser.add_argument("--output","-o",help="path annotation")
parser.add_argument("--inlevel","-il",choices=levels[1:],help="Level of input nodes")
parser.add_argument("--outlevel","-ol",help="Level of annotations")
args = parser.parse_args()


def annotate(df,inlevel,outlevel,startNodes=None):
    if startNodes is None:
        result = df[df["rank"]==inlevel].copy()
    else:
        startNodes = np.array(startNodes).astype(int)
        print("Among {} start nodes".format(startNodes.shape[0]))
        startNodes = np.intersect1d(df.index,startNodes)
        print("{} are presented in NCBI nodes table .".format(startNodes.shape[0]))
        result = df.loc[startNodes,:].copy()
    result[outlevel] = ""
    parentDf = df.loc[result["parent tax_id"].values,:]
    curNodes = result.index
    nStartNodes = result.shape[0]
    nEndNodes = (df["rank"]==outlevel).sum()
    totalEndNodes = 0
    while nEndNodes>0:
        mask = parentDf["rank"]==outlevel
        nEndNodes = mask.sum()
        totalEndNodes += nEndNodes
        print("Get {} nodes in {} nodes or {}%".format(totalEndNodes,nStartNodes,100*np.round(totalEndNodes/nStartNodes,4)))
        endIdx = np.array(parentDf[mask].index)
        pickedNodes = curNodes[mask]
        result.loc[pickedNodes,outlevel] = endIdx
        parentDf = parentDf[~mask]
        parentDf = df.loc[parentDf["parent tax_id"].values,:]
        curNodes = curNodes[~mask]
    print("Done .")
    return result


inlevel = args.inlevel
outlevel = args.outlevel

if inlevel not in levels:
    print("Input level {} do not present in possible classification levels".format(args.inlevel))


parentLevels= list(hierarchy[hierarchy<hierarchy.loc[inlevel]].index)

if outlevel not in parentLevels:
    print("Output level(s) should be parent(s) of input level".format(outlevel))
    print("Levels among $"+" ".join(parentLevels)+"$ should be specified")

print("Load tax data ...")
df = pd.read_csv(args.nodes,sep="\t",header=None,index_col=0)
df = df.iloc[:,:2]
df.columns = ["parent tax_id","rank"]
df.index.name = "tax_id"
print("Done .")


if args.input is not None:
    startNodes = open(args.input).read().strip().split("\n")
    startNodes = [int(i) for  i in startNodes]
else:
    startNodes = None

result = annotate(df,inlevel,outlevel,startNodes)

del result["rank"]

print("Write to output ...")
result.to_csv(args.output,sep="\t")
print("Done .")







