import pandas as pd
import numpy as np
import argparse
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests

parser = argparse.ArgumentParser(description='Performance Fisher test between frequency in two groups')
parser.add_argument('--freq1', '-f1', type=str, required=True, help='first frequency table')
parser.add_argument('--freq2','-f2',type=str,required=True,help='second frequency table')
parser.add_argument('--mincounts','-mc',type=float,help="only counts exceeds this threshold are considered as detected",default=1)
parser.add_argument('--output','-o',type=str,required=True,help='output path')
args = parser.parse_args()


def test(line):
    oddsratio, pvalue = stats.fisher_exact([[line.loc["pos-detected"], line.loc["neg-detected"]], [line.loc["pos-undetected"], line.loc["neg-undetected"]]])
    return pd.Series(dict(logOR=np.log10(oddsratio),p=pvalue))


freq1 = pd.read_csv(args.freq1,sep="\t",index_col=0)
freq2 = pd.read_csv(args.freq2,sep="\t",index_col=0)

n1 = freq1.iloc[0,:].sum()
n2 = freq2.iloc[0,:].sum()

print("{} fusions are in the first freq table".format(freq1.shape[0]))
print("{} fusions are in the second freq table".format(freq2.shape[0]))

freq1 = freq1[freq1["n_detected"]>args.mincounts]
freq2 = freq2[freq2["n_detected"]>args.mincounts]

fusion1 = freq1.index
fusion2 = freq2.index

print("{} fusions are in the first freq table".format(freq1.shape[0]))
print("{} fusions are in the second freq table".format(freq2.shape[0]))

commonFusion = np.intersect1d(fusion1,fusion2)
uniq1 = np.setdiff1d(fusion1,fusion2)
uniq2 = np.setdiff1d(fusion2,fusion1)

print("{} fusions are unique in first group".format(len(uniq1)))
print("{} fusions are commonly detected".format(len(commonFusion)))
print("{} fusions are unique in second group".format(len(uniq2)))

allFusions = set(fusion1).union(fusion2)

freqTable = pd.DataFrame(index=allFusions,columns=["pos-detected","pos-undetected","neg-detected","neg-undetected"])
freqTable.loc[fusion1,"pos-detected"] = freq1.loc[fusion1,"n_detected"]
freqTable.loc[fusion1,"pos-undetected"] = freq1.loc[fusion1,"n_undetected"]
freqTable.loc[fusion2,"neg-detected"] = freq2.loc[fusion2,"n_detected"]
freqTable.loc[fusion2,"neg-undetected"] = freq2.loc[fusion2,"n_undetected"]
freqTable.loc[uniq2,"pos-detected"] = 1.0
freqTable.loc[uniq2,"pos-undetected"] = n1-1.0
freqTable.loc[uniq1,"neg-detected"] = 1.0
freqTable.loc[uniq1,"neg-undetected"] = n2-1.0

diffTable = freqTable.apply(test,axis=1)
diffTable["padj"] = multipletests(diffTable["p"],method="fdr_bh")[1]
print(diffTable[diffTable["p"]<0.05])
diffTable.to_csv(args.output,sep="\t")

