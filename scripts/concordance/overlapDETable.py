import pandas as pd
import argparse
import sys
import numpy as np

parser = argparse.ArgumentParser(description='Overlap Two Defferentially Expressed Table')
parser.add_argument('--table1', '-t1', type=str, required=True, help='the first de table')
parser.add_argument('--table2','-t2',type=str,required=True,help='the second de table')
parser.add_argument('--label1','-l1',type=str,required=True,help='label of first de table')
parser.add_argument('--label2','-l2',type=str,required=True,help='label of second de table')
parser.add_argument('--padjcutoff','-padj',type=float,default=0.05)
parser.add_argument('--diffkey','-k',type=str,default="log2FoldChange")
parser.add_argument('--diffcutoff','-d',type=float,default=1,help="cutoff for difference")
parser.add_argument('--method','-m',choices=["threshold","topgene"],default="threshold",help="Which method to use to retrive diff genes")
parser.add_argument('--output','-o',type=str,required=True,help='output path')
parser.add_argument('--options','-ops',type=str,choices=["first","second","both"],default="both")
parser.add_argument('--stat',type=str,default=None,help="where to output the statistis")
parser.add_argument("--strip",action="store_true",help="Whether strip gene ids",default=False)
args = parser.parse_args()

def loadData(path,trim=False):
    df = pd.read_csv(path,sep="\t",index_col=0)
    if not trim:
        return df
    else:
        df.index = df.index.map(lambda x:x.split("|")[0].split(".")[0])
        df = df[~df.index.duplicated()]
        return df


df1 = loadData(args.table1,trim=args.strip)
df2 = loadData(args.table2,trim=args.strip)

print("{} genes in first de table".format(df1.shape[0]))
print("{} genes in second de table".format(df2.shape[0]))


commonGenes = np.intersect1d(df1.index,df2.index)

if args.method == "threshold":
    df1up = df1[(df1[args.diffkey]>args.diffcutoff)&(df1["padj"]<args.padjcutoff)]
    df2up = df2[(df2[args.diffkey]>args.diffcutoff)&(df2["padj"]<args.padjcutoff)]
    df1down = df1[(df1[args.diffkey]<-args.diffcutoff)&(df1["padj"]<args.padjcutoff)]
    df2down = df2[(df2[args.diffkey]<-args.diffcutoff)&(df2["padj"]<args.padjcutoff)]
elif args.method == "topgene":
    print("remained to be implemented ..")
    sys.exit(0)

stat = pd.DataFrame(index=[args.label1+"-down",args.label1+"-up",args.label1+"-null"],columns=[args.label2+"-down",args.label2+"-up",args.label2+"-null"])

print("{} genes up in {}".format(df1up.shape[0],args.label1))
stat.loc[args.label1+"-up",args.label2+"-null"] = df1up.shape[0]
print("{} genes down in {}".format(df1down.shape[0],args.label1))
stat.loc[args.label1+"-down",args.label2+"-null"] = df1down.shape[0]
print("{} genes up in {}".format(df2up.shape[0],args.label2))
stat.loc[args.label1+"-null",args.label2+"-up"] = df2up.shape[0]
print("{} genes down in {}".format(df2down.shape[0],args.label2))
stat.loc[args.label1+"-null",args.label2+"-down"] = df2down.shape[0]


commonUp = np.intersect1d(df1up.index,df2up.index)
commonDown = np.intersect1d(df1down.index,df2down.index)
up1Down2 = np.intersect1d(df1up.index,df2down.index)
down1Up2 = np.intersect1d(df1down.index,df2up.index)
common = list(commonUp) + list(commonDown)

columns = [args.label1+"-"+args.diffkey,args.label1+"-padj",args.label2+"-"+args.diffkey,args.label2+"-padj"]
res = pd.DataFrame(index=common,columns=columns)
res.loc[common,args.label1+"-"+args.diffkey] = df1.loc[common,args.diffkey]
res.loc[common,args.label2+"-"+args.diffkey] = df2.loc[common,args.diffkey]

res.loc[common,args.label1+"-padj"] = df1.loc[common,"padj"]
res.loc[common,args.label2+"-padj"] = df2.loc[common,"padj"]

print("{} genes commonly up".format(len(commonUp)))
stat.loc[args.label1+"-up",args.label2+"-up"] = len(commonUp)
print("{} genes commonly down".format(len(commonDown)))
stat.loc[args.label1+"-down",args.label2+"-down"] = len(commonDown)

stat.loc[args.label1+"-up",args.label2+"-down"] = len(up1Down2)
stat.loc[args.label1+"-down",args.label2+"-up"] = len(down1Up2)

stat.loc[args.label1+"-null",args.label2+"-null"] = len(commonGenes)

if args.options == "both":
    res.to_csv(args.output,sep="\t")
elif args.options == "first":
    res = res.loc[:,[args.label1+"-padj",args.label1+"-"+args.diffkey]]
    res.columns = ["padj",args.diffkey]
    res.to_csv(args.output,sep="\t")
elif args.options == "second":
    res = res.loc[:,[args.label2+"-padj",args.label2+"-"+args.diffkey]]
    res.columns = ["padj",args.diffkey]
    res.to_csv(args.output,sep="\t")

stat.to_csv(args.stat,sep="\t")
