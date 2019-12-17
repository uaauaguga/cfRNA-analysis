import pandas as pd
import numpy as np
import argparse
from itertools import product

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input_dir',help='Dirs contain differential expression result',required=True)
parser.add_argument('-c','--comparisons',help="Files for comparisons between classes, comparison should be named as the file name of each de table, trimmed off .txt",required=True)
parser.add_argument('-o','--bool_mat',help='Bool value coded matrix, indicating whether up/down for certain comparison',required=True)
parser.add_argument('-d','--diff',help='Absolute value of log2foldchange cut off for DE, abs(delta(psi)) for AS, abs(delta(ratio)) for editing ratio, etc',default=1.0,type=float)
parser.add_argument('-q','--padj',help='Threshold for adjusted p value',default=0.05,type=float)
parser.add_arguemnt('-dk','--diff_key',help='Which columns in the de table measures difference',default="log2FoldChange")
parser.add_argument('-qk','--padj_key',help='Which columns in the de table measures padj',default="padj")
parser.add_argument('-t','--trend',help='Whether include trend information',choices=["up","down","both","merge"],default="both")
args = parser.parse_args()

indir = args.input_dir
comparisonsPath = args.comparisons
outmat = args.bool_mat
diff = args.diff
padj = args.padj
#PValue FDR IncLevelDifference
comparisons = open(comparisonsPath).read().strip().split("\n")


diffCol= args.diff_key
padjCol=args.padj_key

def loadDiffTable(path,diff=1,padj=0.05):
    global diffCol
    global padjCol
    diffTable = pd.read_csv(path,index_col=0,sep="\t")
    return diffTable[(diffTable[diffCol].abs()>diff) & (diffTable[padjCol]<padj)]


def extractTrends(diffTable):
    global diffCol
    up = (diffTable[diffCol]>0).astype(int)
    down = (diffTable[diffCol]<0).astype(int)
    df = pd.DataFrame({"IDs":diffTable.index,"up":up,"down":down})
    df = df.set_index("IDs")
    return df

def summarize(diffTableDir,trend="both"):
    diffTablePath = diffTableDir + "/{}.txt"
    all_genes = set()
    global comparisons
    global diff
    global padj
    sumDict = {}
    for comparison in comparisons:
        print("Processing {} ...".format(comparison))
        diffTable = loadDiffTable(path=diffTablePath.format(comparison),diff=diff,padj=padj)
        trend = extractTrends(diffTable)
        sumDict[comparison] = trend
        all_genes = all_genes.union(set(trend.index))
    if trend == "merged":
        columns = comparisons
    else:
        upCols = [comp+"-up" for comp in comparisons]
        downCols = [comp+"-down" for comp in comparisons]
        columns= upCols + downCols
    sumTable = pd.DataFrame(index=all_genes,columns=columns)
    trends=["up","down"]
    columns=[comp+"-"+trend for comp,trend in product(comparisons,trends)]
    sumTable = pd.DataFrame(index=all_genes,columns=columns)
    for comparison in comparisons:
        if trend == "merged":
            sumTable.loc[sumDict[comparison].index,comparison] = int((sumDict[comparison]["up"]+sumDict[comparison]["down"])>1)
        else:
            sumTable.loc[sumDict[comparison].index,comparison+"-up"] = sumDict[comparison]["up"]
            sumTable.loc[sumDict[comparison].index,comparison+"-down"] = sumDict[comparison]["down"]
    if trend == "up":
        return sumTable.fillna(0).loc[:,upCols]
    if trend == "down":
        return sumTable.fillna(0).loc[:,downCols]
    return  sumTable.fillna(0)

result = summarize(indir,args.trend)
result.to_csv(outmat,sep="\t")
