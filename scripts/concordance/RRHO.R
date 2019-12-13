library(lattice)
library(dplyr)
library(RRHO)
library("optparse")

option_list <- list(make_option(c("--table1"),type="character",help="path of first difference table, make sure the first column contains no duplicates"),
                    make_option(c("--table2"),type="character",help="path of second difference table"),
		    make_option(c("--label1"),type="character",help="label of first table"),
		    make_option(c("--label2"),type="character",help="laabel of second table"),
		    make_option(c("-k","--diffkey"),default="log2FoldChange",type="character",help="which column to use for ranking"),
		    make_option(c("-o","--outfig"),type="character",help="output figure path"),
		    make_option(c("-p","--logp"),type="character",help="output p value path"))
opt <- parse_args(OptionParser(option_list=option_list))


de.table.1.path <- opt$table1
de.table.2.path <- opt$table2
diff1 <- opt$label1
diff2 <- opt$label2
outfig <- opt$outfig



de.table.1 <- read.table(de.table.1.path,header=TRUE,sep="\t",check.names = FALSE,stringsAsFactors = F,row.names=1)
de.table.2 <- read.table(de.table.2.path,header=TRUE,sep="\t",check.names = FALSE,stringsAsFactors = F,row.names=1)


common.gene.id <- intersect(rownames(de.table.1),rownames(de.table.2))
cat(paste(c(length(rownames(de.table.1))," are provided from table 1\n")))
cat(paste(c(length(rownames(de.table.2))," are provided from for table 2\n")))
cat(paste(c(length(common.gene.id)," are finally used for RRHO\n")))

de.table.1.used <- de.table.1[common.gene.id,]
de.table.1.rank <- de.table.1.used[,opt$diffkey,drop=F] 
de.table.1.rank <- tibble::rownames_to_column(de.table.1.rank, "gene")
de.table.2.used <- de.table.2[common.gene.id,]
de.table.2.rank <- de.table.2.used[,opt$diffkey,drop=F] 
de.table.2.rank <- tibble::rownames_to_column(de.table.2.rank, "gene")

RRHO.res <-  RRHO(de.table.1.rank,de.table.2.rank,  alternative='enrichment',labels=c(diff1,diff2),log10.ind=TRUE)
coul <- colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan", "#7FFF7F", "yellow", "#FF7F00", "red", "#7F0000"))
#coul <- colorRampPalette(c("white", "red"))(50)
res <- RRHO.res$hypermat
write.table(res,file=opt$logp,sep="\t",col.names=F,row.names=F)
n.ticks <- nrow(res)
pdf(outfig)
        pos.down <- as.integer(n.ticks*4/5)
        pos.up <- as.integer(n.ticks/5)
	print(pos.up)
        lattice::levelplot(res, 
		   col.regions = coul,
		   xlab=list(label=diff1,fontsize=20,fontface='bold'),
		   ylab=list(label=diff2,fontsize=20,fontface='bold'),
		   scales=list(x=list(at=c(pos.up,pos.down),labels=c("up","down"),ce=1.45,fontface='bold'),
		   	       y=list(at=c(pos.up,pos.down),labels=c("up","down"),ce=1.45,fontface='bold'),tck = c(0,0)),
		   cuts = 10,
		   pretty = T,
		   main=list(paste0(diff1,"-",diff2),fontsize=24))

dev.off()
