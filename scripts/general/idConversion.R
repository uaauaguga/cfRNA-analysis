Args = commandArgs(TRUE)
input = Args[1]
output = Args[2]
library(org.Hs.eg.db)
library(biomaRt)

#get all ensembl genes
ensembl <- useMart("ensembl",dataset="hsapiens_gene_ensembl") 

#input my gene_list 
input.list<-read.table(input)
input.list.convert <- getBM(attributes=c('ensembl_gene_id', 'entrezgene_id'), filters = 'ensembl_gene_id', values = input.list, mart = ensembl)
output.list<-as.character(input.list.convert[,2])
write.table(output.list,file=output,sep="\t", quote=F,row.names=F,col.names=F)

