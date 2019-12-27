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
parser.add_argument('-m','--method',help='Which method used for summarize detable',choices=["top","threshold"],default="threshold")
parser.add_argument('-n','--topNgene',help='How many genes to select',default=20)
parser.add_argument('-dk','--diff_key',help='Which columns in the de table measures difference',default="log2FoldChange")
parser.add_argument('-qk','--padj_key',help='Which columns in the de table measures padj',default="padj")
parser.add_argument('-t','--trend',help='Whether include trend information',choices=["up","down","both","merged"],default="both")
parser.add_argument('--stat',help='where to output summarize statistics',default=None)
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

def loadDiffTableThreshold(path,diff=1,padj=0.05):
    global diffCol
    global padjCol
    diffTable = pd.read_csv(path,index_col=0,sep="\t")
    return diffTable[(diffTable[diffCol].abs()>diff) & (diffTable[padjCol]<padj)]


def loadDiffTableTopN(path,n=20):
    global diffCol
    global padjCol
    diffTable = pd.read_csv(path,index_col=0,sep="\t")
    diffTable["pi"] = -diffTable[diffCol]*np.log10(diffTable[padjCol])
    diffTable = diffTable.sort_values("pi",ascending=False)
    topGene = diffTable.iloc[:n,:].index
    bottomGene = diffTable.iloc[-n:,:].index
    genes = list(topGene) + list(bottomGene)
    return diffTable.loc[genes,:]

def extractTrends(diffTable):
    global diffCol
    up = (diffTable[diffCol]>0).astype(int)
    down = (diffTable[diffCol]<0).astype(int)
    print("{} up, {} down".format(up.sum(),down.sum()))
    df = pd.DataFrame({"IDs":diffTable.index,"up":up,"down":down})
    df = df.set_index("IDs")
    return df

def summarize(diffTableDir,usedTrend=args.trend):
    diffTablePath = diffTableDir + "/{}.txt"
    all_genes = set()
    global comparisons
    global diff
    global padj
    sumDict = {}
    for comparison in comparisons:
        print("Processing {} ...".format(comparison))
        if args.method == "threshold":
            diffTable = loadDiffTableThreshold(path=diffTablePath.format(comparison),diff=diff,padj=padj)
        elif args.method == "top":
            diffTable = loadDiffTableTopN(path=diffTablePath.format(comparison),n=args.topNgene)
        trend = extractTrends(diffTable)
        sumDict[comparison] = trend
        all_genes = all_genes.union(set(trend.index))
    if usedTrend == "merged":
        columns = comparisons
    else:
        upCols = [comp+"-up" for comp in comparisons]
        downCols = [comp+"-down" for comp in comparisons]
        columns= upCols + downCols
    sumTable = pd.DataFrame(index=all_genes,columns=columns)
    for comparison in comparisons:
        if usedTrend == "merged":
            sumTable.loc[sumDict[comparison].index,comparison] = ((sumDict[comparison]["up"]+sumDict[comparison]["down"])>0).astype(int)
        else:
            sumTable.loc[sumDict[comparison].index,comparison+"-up"] = sumDict[comparison]["up"]
            sumTable.loc[sumDict[comparison].index,comparison+"-down"] = sumDict[comparison]["down"]
    if usedTrend == "up":
        temp =  sumTable.fillna(0).loc[:,upCols]
        return temp[temp.sum(axis=1)>0].sort_values(list(temp.columns),ascending=False)
    if usedTrend == "down":
        temp =  sumTable.fillna(0).loc[:,downCols]
        return temp[temp.sum(axis=1)>0].sort_values(list(temp.columns),ascending=False)
    return  sumTable.fillna(0)

result = summarize(indir,args.trend)
result.to_csv(outmat,sep="\t")
if args.stat is not None:
    result.sum(axis=0).to_csv(args.stat,sep="\t")
