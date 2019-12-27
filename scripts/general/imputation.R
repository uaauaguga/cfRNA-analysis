#For imputation
suppressPackageStartupMessages(library(argparse))
library(DrImpute)
parser <- ArgumentParser(description='For matrix imputation')
parser$add_argument('-i', '--matrix', type='character', required=TRUE,
                    help='input count matrix. Rows are genes. Columns are samples.')
#parser$add_argument('-t', '--table', type='character', 
#                    help='input table contains sample class information')
#parser$add_argument('-k', '--key', type='character', 
#                    help='key used in the sample info table')
#parser$add_argument('-m', '--method', type='character', default="drimpute",choices=c('median','mean','drimpute'),
#                    help='differential expression method to use')
parser$add_argument('-o', '--output-file', type='character', required=TRUE,
                    help='output file')
args <- parser$parse_args()

#if(args$method %in% c('median','mean')){stop("Sample classes are required")}


#impute <- function(data,sample.classes=sample.classes,method="median"){
#  for(type in types){
#    sample.ids <- rownames(sample.classes)[sample.class==type]
#    sub.data <- data[sample.ids]
#    na.ids <- names(sub.data)[is.na(sub.data)]
#    non.na.ids <- names(sub.data)[!is.na(sub.data)]
#    respresent <- median(as.numeric(data[non.na.ids]))
#    data[na.ids] <- respresent
#  }
#  return(data)
#}
#impute.wrap <- function(data){impute(data,sample.class)}

#args <- list()
#args$matrix <- "/home/jinyunfan/Documents/bioinfo/pico-analysis/variations/editing/1226/cfRNA/temp.txt"
#args$table <- "/home/jinyunfan/Documents/bioinfo/pico-analysis/covariates/covariates.txt"
#args$key <- "Disease"
mat <-read.table(args$matrix,sep="\t",header=T,row.names=1,check.names = F)
#info <- read.table(args$table,sep="\t",header=T,row.names=1)
#sample.classes <- info[,args$key,drop=F]
cat(length(colnames(mat))," samples are provided in the input matrix")
#cat(length(rownames(info))," samples are provided in the sample info table")
#common.samples <- intersect(colnames(mat),rownames(info))
#cat(length(common.samples)," samples are in common")
#mat <- mat[,common.samples]
mat <- as.matrix(mat)
#sample.classes <- sample.classes[common.samples,,drop=F]
res <- DrImpute(as.matrix(mat))
write.table(res,file=args$output_file,sep="\t")


