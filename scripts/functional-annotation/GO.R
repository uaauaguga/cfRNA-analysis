library(clusterProfiler)
library(org.Hs.eg.db)
args<-commandArgs(TRUE)
infile <- args[1]
outfile <- args[2]
gene.list <- as.character(read.table(infile)[,1])
go <- enrichGO(gene.list, OrgDb = org.Hs.eg.db, ont='BP',pAdjustMethod = 'BH',pvalueCutoff = 1, qvalueCutoff = 1,keyType = 'ENTREZID')
write.table(go,file=outfile,sep="\t",quote=FALSE)
