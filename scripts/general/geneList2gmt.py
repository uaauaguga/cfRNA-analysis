import argparse
parser = argparse.ArgumentParser(description="convert gene list to .gmt file")
parser.add_argument("--list","-l",required=True,help="paths for input gene lists")
parser.add_argument("--output","-o",required=True,help="path for output gmt file")
parser.add_argument("--setname","-s",required=True,help="gene set name")
parser.add_argument("--notation","-n",required=True,help="the second column of gmt file")
args = parser.parse_args()

gene_ids = open(args.list).read().strip().split("\n")
setname = args.setname
notation = args.notation

line = [setname] + [notation] + gene_ids

with open(args.output,"w") as f:
    f.write("\t".join(line)+"\n")
