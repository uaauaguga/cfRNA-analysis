# cfRNA-analysis
## Reads Preprocessing

Adapter sequences in the raw sequencing data were removed using cutadapt with parameter -q 30,30 AGATCGGAAGAGCACACGTCTGAACTCCAGTCA  AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT --trim-n -m 30. The template switch oligo (TSO) sequences were then trimmed with a customized python script, reads shorter than 30 nt were discarded. The remaining reads were mapped to spike in library, NCBI's UniVec Core sequences, human rRNA sequences with STAR aligner in a sequential manner. 

## Quality Control and Transcriptome Quantification

  We used STAR aligner to map cleaned reads to hg38 genome index build with gencodev27 splice junction annotation. The unmapped reads were mapped to upstream and downstream 300 nt sequence around trans-splice junction extracted from circBase. Duplications in genome and circular RNA mapped reads were removed with picard tools MarkDuplicates. To estimate the distribution of genome mapped reads along different genomic regions, reads were assigned one of several classes with bedtools follow the priority: lncRNA, mRNA, tucpRNA, srpRNA, snRNA, snoRNA, Y_RNA, other exon regions, intron, antisense, promoter, enhancer, and repeats. Here we use mitranscriptome annotation to define the genomic regions correspond to lncRNA and tucpRNA; regions of mRNA, srpRNA, snRNA, snoRNA and Y_RNA were specified with gencodev27 annotation in a similar way. Antisense is defined as reverse strand of exons. Repeat regions were download from UCSC GenomeBrowser, promoter and enhancer regions were retrived from Broad ChromHMM annotations. 
  We count genome mapped reads using featureCounts, with mRNA,YRNA,snoRNA,snRNA srpRNA annotation in genecode v27 and lncRNA annotation in mitranscriptome (tucpRNA is excluded from further analysis because of its un-well characterized nature). Genes with TPM higher than 2 were considered as detectable. The trans-spliced juntion mapped reads were quantified with a customized python script. Differential expression between each cancer types and healthy donors was performed using glmlrt method in edgeR package.

## Post-transcriptional modification analysis

 Here we use percentage spliced in (psi) value estimated by rMATs software as a surrogate for the relative abundance of differentially spliced isoforms. Differentially spliced genes were determined by cutoff using rMAT's build in statistical testing methods. 
 Differential alternative polyadenylation analysis was performed using DaPar scripts with default parameter. 
 RNAEditor was utilized for RNA editing analysis. Due to the limited sequencing coverage, 

## Other RNA variation analysis
  STAR-fusion
  SNP

## Discovery-Validation Splitting
  Samples from healthy donors and patients with different cancer types were stratified according to sample sources (from which hospital), genders, ages and cancer subtypes, then split into two dataset in 1:1 manner.


