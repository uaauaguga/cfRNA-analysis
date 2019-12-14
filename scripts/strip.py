import pandas as pd
import argparse
parser = argparse.ArgumentParser(description='Strip gene index to ensid without version information, for expresion matrix or detable')
parser.add_argument('--input', '-i', type=str, required=True, help='input matrix')
parser.add_argument('--output','-o',type=str,required=True,help='output path')
args = parser.parse_args()

def loadData(path):
    df = pd.read_csv(path,sep="\t",index_col=0)
    df.index = df.index.map(lambda x:x.split("|")[0].split(".")[0])
    df = df[~df.index.duplicated()]
    return df

loadData(args.input).to_csv(args.output,sep="\t")

