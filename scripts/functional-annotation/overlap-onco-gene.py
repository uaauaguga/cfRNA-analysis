import pandas as pd
import numpy as np
import argparse
import sys
from scipy.stats import hypergeom
parser = argparse.ArgumentParser(description='Overlap Between gene list and given gene set ')
parser.add_argument('--list', '-l', type=str, required=True, help='input gene list')
parser.add_argument('--set','-s',type=str,required=True,help="input gene set")
parser.add_argument('--background','-bg',type=str,help="background gene list")
parser.add_argument('--method','-m',default="ratio",choices=["ratio","ratio_bg"],help="specify output")
args = parser.parse_args()


geneList = open(args.list).read().strip().split("\n")
geneSet = open(args.set).read().strip().split("\n")
backgroundSet = open(args.background).read().strip().split("\n")


if args.method=="ratio_bg" and args.background==None:
    print("The background gene list should be provided using ratio_bg")
    sys.exit(0)


if args.method == "ratio":
    n = len(geneSet)
    m = np.intersect1d(geneList,geneSet).shape[0]
    print(m/n)
elif args.method == "ratio_bg":
    M = len(backgroundSet)
    usedGeneSet = np.intersect1d(backgroundSet,geneSet)
    n = usedGeneSet.shape[0]
    N = len(geneList)
    m = np.intersect1d(geneList,usedGeneSet).shape[0]
    p = 1-hypergeom(M=M,n=n,N=N).cdf(m)
    print(m/n,p)



