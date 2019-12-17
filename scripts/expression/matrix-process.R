#!/usr/bin/env Rscript
suppressPackageStartupMessages(library("argparse"))
suppressPackageStartupMessages(library("edgeR"))
# create parser object
parser <- ArgumentParser()
parser$add_argument("-i", "--input", required=TRUE, help="input expression matrix file")
parser$add_argument("-o", "--output", required=TRUE, help="output expression matrix file")
parser$add_argument("-m", "--method", required=TRUE, help="name of the method")
args <- parser$parse_args()
read_matrix <- function(filename){
    read.table(filename, sep='\t', header=TRUE,  check.names=FALSE, row.names=1, stringsAsFactors=FALSE)
}
write_matrix <- function(mat, filename){
    write.table(mat, filename, sep='\t',quote=FALSE, row.names=TRUE, col.names=TRUE)
}

print(args$method)

normalize <- function(mat,method,top_n = 20) {
    if (method == 'TMM')       mat <- norm_tmm(mat)
    else if (method == 'RLE')       mat <- norm_rle(mat)
    else if (method == 'CPM')       mat <- norm_cpm(mat)
    else if (method == 'UQ')        mat <- norm_uq(mat)
    else if (method == 'CPM_top')   mat <- norm_cpm_top(mat, top_n)
    else if (method == 'TPM')       mat <- norm_tpm(mat)
    else if (method == 'FPKM')      mat <- norm_fpkm(mat)
    else stop('unknown normalization method: ', method)
    mat
}
norm_uq <- function(mat) {
    print('start normalization using UQ')
    dl <- edgeR::DGEList(counts=mat)
    dl <- edgeR::calcNormFactors(dl, method='upperquartile')
    edgeR::cpm(dl)
}
norm_tmm <- function(mat) {
    print('start normalization using TMM')
    dl <- edgeR::DGEList(counts=mat)
    dl <- edgeR::calcNormFactors(dl, method='TMM')
    return(edgeR::cpm(dl))
}

norm_rle <- function(mat) {
    print('start normalization using RLE')
    dl <- edgeR::DGEList(counts=mat)
    dl <- edgeR::calcNormFactors(dl, method='RLE')
    edgeR::cpm(dl)
}

norm_cpm_top <- function(mat, top_n) {
    print(paste('start normalization using top',top_n,'genes as scale factor',sep=' '))
    if (nrow(mat) < top_n)
    stop('too few feature for CPM top n normalization')
    
    row_top <-  mat %>% rowSums() %>% sort(decreasing = T, index.return = T) %>%
    {.$ix[seq_len(top_n)]}
    
    top = t(t(mat[row_top,]*1e6) / colSums(mat[row_top, , drop = F], na.rm = T))
    top_down= t(t(mat[setdiff(seq_len(dim(mat)[1]),row_top),]*1e6) / colSums(mat[setdiff(seq_len(dim(mat)[1]),row_top), , drop = F], na.rm = T))
    mat_top <- rbind(top,top_down)
    mat_top[rownames(mat),]
}

norm_cpm <- function(mat) {
    t(t(mat*1e6)/colSums(mat))
}

norm_fpkm <- function(mat) {
    genes <- rownames(mat)
    genes.length <- unlist(lapply(genes,
    function(x) { data <- strsplit(x,"\\|")[[1]]
    len <- length(data)
    as.numeric(data[len])}))
    mat <- t(t(mat*1e6)/colSums(mat))
     (mat*1e3)/genes.length
}

norm_tpm <- function(mat) {
    genes <- rownames(mat)
    genes.length <- unlist(lapply(genes,
   function(x){
   data <- strsplit(x,"\\|")[[1]]
   len <- length(data)
   as.numeric(data[len])}))
   mat <- mat/genes.length
   t(t(mat*1e6)/colSums(mat))
}

message('read expression matrix: ', args$input)
mat <- read_matrix(args$input)
mat <- normalize(mat,args$method)
message('write expression matrix: ', args$output)
write_matrix(mat, args$output)
