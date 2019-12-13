library("ComplexHeatmap")
library("circlize")
df <- read.table("~/Documents/bioinfo/pico-analysis/functional-annotation/KEGG/clusterProfilter-result/KEGG-for-plot-v2.tsv",sep="\t",header=TRUE,row.names = 1)
cancers <- c("expression.CRC","expression.HCC","expression.LC","expression.GC","expression.EC")
df <- df[,cancers]
features <- unlist(lapply(colnames(df),function(x){strsplit(x,"\\.")[[1]][1]}))
cancers <- unlist(lapply(colnames(df),function(x){strsplit(x,"\\.")[[1]][2]}))
#features <- factor(features,level=c("expression","splicing","editing"))
#cancers <- factor(cancers,level=c("CRC","EC","HCC","LC"))



col_fun = colorRamp2(c(0,10), c("white", "#E41A1C"))
#Heatmap(as.matrix(df),cluster_rows = F,border=T,column_labels=cancers,cluster_columns=F,column_split =features,col = col_fun,name="-log10p",column_names_side="top")

Heatmap(as.matrix(df),cluster_rows = F,
        border=T,
        column_labels=cancers,
        cluster_columns=F,
        column_split =features,
        col = col_fun,
        name="-log10p\n",
        column_names_side="top",
        column_title_gp = gpar(fontsize = 20),
        column_names_gp = gpar(fontsize = 20),
        column_names_centered =T)



