library("ComplexHeatmap")
library("circlize")
cancers=c("CRC","HCC","LC","GC","EC")
AS.df <- read.table("/home/jinyunfan/Documents/bioinfo/pico-analysis/functional-annotation/overlap/AS.txt",header=TRUE,row.names = 1)[,cancers]
exp.df <- read.table("/home/jinyunfan/Documents/bioinfo/pico-analysis/functional-annotation/overlap/exp.txt",header=TRUE,row.names = 1)[,cancers]
editing.df <- read.table("/home/jinyunfan/Documents/bioinfo/pico-analysis/functional-annotation/overlap/editing.txt",header=TRUE,row.names = 1)[,cancers]
features <-  c(rep("expression",5),rep("splicing",5),rep("editing",5))
features <- factor(features,level=c("expression","splicing","editing"))
df <- cbind(exp.df,AS.df,editing.df)
topAno = HeatmapAnnotation(variations=features)
col_fun = colorRamp2(c(0, 0.09,0.18), c("#377EB8", "white", "#E41A1C"))
geneSet <- factor(c(rep("pos",7),rep("neg",3)),level=c("pos","neg"))
Heatmap(as.matrix(df),
        cluster_rows = F,
        border=T,
        cluster_columns=F,
        column_split =features,
        row_split=geneSet ,
        col = col_fun,
        name="Normalized Overlap",
        column_names_side="top",
        column_names_gp = gpar(fontsize = 20),
        row_title_gp = gpar(fontsize = 20),
        column_title_gp = gpar(fontsize = 24), 
        row_names_gp = gpar(fontsize = 20))



