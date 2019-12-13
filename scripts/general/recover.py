import pandas as pd
import argparse
parser = argparse.ArgumentParser(description='Recover ENSG ID to exSeek ID')
parser.add_argument('--input', '-i', type=str, required=True, help='input matrix')
parser.add_argument('--output','-o',type=str,required=True,help='output path')
parser.add_argument('--mapping','-m',type=str,default="~/Documents/bioinfo/pico-analysis/id-mapping.txt")
args = parser.parse_args()

df = pd.read_csv(args.input,sep="\t",index_col=0)
df = df[~df.index.duplicated()]
mapping = pd.read_csv(args.mapping,sep="\t",index_col=0)
mapping = mapping[~mapping.index.duplicated()]
df.index = mapping.loc[df.index,"long_id"]
df.to_csv(args.output,sep="\t")
