library("ggplot2")
args <- commandArgs(TRUE)
infile <- args[1]
outfile <- args[2]
infile <- "data/deseq2-1-null-for-bar-plot.txt"
infile <- "/home/jinyunfan/Documents/bioinfo/pico-analysis/barplot/deseq2-1.txt"
plotTable <- read.table(infile,header=TRUE,sep="\t")



##For all trend 
infile <- "/home/jinyunfan/Documents/bioinfo/pico-analysis/barplot/data/updownPlot-v2.txt"
infile <- "/home/jinyunfan/Documents/bioinfo/pico-analysis/figures/1112/barplot/summary.txt"
plotTable <- read.table(infile,header=TRUE,sep="\t")
#plotTable$feature <- factor(plotTable$feature,levels=c("differential expression","alternative splicing","RNA editing"))
plotTable$feature <- factor(plotTable$feature,levels=c("expression","splicing","editing"))
plotTable$trend <- factor(plotTable$trend,levels=c("up","down"))
plotTable$disease <- factor(plotTable$disease,levels=c("CRC","HCC","LC","GC","EC"))
#g <- ggplot(data=plotTable,aes(x=disease,y=num,fill=trend)) + geom_bar(stat="identity",width=0.6,color="black") + facet_wrap(~feature,nrow=3,ncol=1,scales="free") + scale_fill_manual(values=c("#1C1C75","#CCEEFF"))+theme_classic()
g <- ggplot(data=plotTable,aes(x=disease,y=num,fill=trend)) +
	 geom_bar(stat="identity",width=0.6,color="black") +
	  #facet_wrap(~feature,nrow=3,ncol=1,scales="free",strip.position="right") +
	  facet_wrap(~feature,nrow=3,scales="free") +
	   scale_fill_manual(values=c("#104E8B","#BCD2EE")) + 
	    theme_classic() + 
	     theme(strip.text = element_text(size = 15),
		    axis.text = element_text( size = 14,color="black"),
		     axis.text.x = element_text(face="bold"),
		     axis.title = element_text(size =16, face="bold"),
		      panel.border = element_rect(color="black",fill=NA,size=1.5),
		      strip.background = element_rect(color="black",fill=NA,size=1.5),
		       axis.line = element_blank()
		       )
 


#for diff-exp
infile <- "/home/jinyunfan/Documents/bioinfo/pico-analysis/variations/expression/trouble-shoot/test-methods/collapsed/final.txt"
plotTable <- read.table(infile,header=TRUE,sep="\t")
plotTable$disease <- factor(plotTable$disease,levels=c("CRC","HCC","LC","GC","EC"))
g <- ggplot(data=plotTable,aes(x=trend,y=num,fill=rnaType)) + 
  geom_bar(stat="identity",width=0.8,color="black") + 
  facet_wrap(~disease,ncol=5) + 
  theme_classic() +
  theme(strip.text = element_text(size = 20),
        axis.text = element_text( size = 15,color="black"),
        axis.title = element_text(size =20, face="bold"),
        panel.spacing.x =unit(0.3, "lines"),
        strip.background = element_rect(color="black",fill=NA,size=1.5),
        axis.line = element_blank())
#For diff-AS
#plotTable <- read.table(infile,header=TRUE,row.names=1)
#g <- ggplot(data=plotTable,aes(x=pos,y=num,fill=AS.event)) + geom_bar(stat="identity") + facet_wrap(~trend) + theme_classic()
#ggsave(g,file=outfile,width=8,height=4)

#For editing
g <- ggplot(data=plotTable,aes(x=pos,y=num,fill=trend)) + geom_bar(stat="identity") + facet_wrap(~state) + theme_classic()
ggsave(g,file=outfile,width=8,height=4) 




g <- ggplot(data=plotTable,aes(x=disease,y=num,fill=trend)) + geom_bar(stat="identity",width=0.8,color="black") + facet_wrap(~feature,nrow=3,ncol=1,scales="free") +theme_classic()

