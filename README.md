# cfRNA-analysis
## Reads Preprocessing

  Adapter sequences in the raw sequencing data were removed using cutadapt with parameter -q 30,30 AGATCGGAAGAGCACACGTCTGAACTCCAGTCA   AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT --trim-n -m 30. The template switch oligo (TSO) sequences were then trimmed with a customized python script, reads shorter than 30 nt were discarded. The remaining reads were mapped to spike-in library, NCBI's UniVec Core sequences, human rRNA sequences with STAR aligner in a sequentially. 

## Quality Control and Transcriptome Quantification

  We used STAR aligner to map cleaned reads to hg38 genome index build with gencodev27 splice junction annotation. The unmapped reads were mapped to upstream and downstream 300 nt sequence around trans-splice junction extracted from circBase. Duplications in genome and circular RNA mapped reads were removed with picard tools MarkDuplicates. To estimate the distribution of genome mapped reads along different genomic regions, reads were assigned one of several classes with bedtools follow the priority: lncRNA, mRNA, tucpRNA, srpRNA, snRNA, snoRNA, YRNA, other exon regions, intron, antisense, promoter, enhancer, and repeats. Here we use mitranscriptome annotation to define the genomic regions correspond to lncRNA and tucpRNA; regions of mRNA, srpRNA, snRNA, snoRNA and YRNA were specified refer to gencodev27 annotation in a similar way. Antisense is defined as the reverse strand of exons regions. Repeat regions were download from UCSC GenomeBrowser. Promoter and enhancer regions were retrived from Broad ChromHMM annotations. 
  Genome mapped reads were assiged to genomics features with featureCounts, using mRNA,YRNA,snoRNA,snRNA srpRNA annotation in genecode v27, and lncRNA annotation in mitranscriptome (tucpRNA is excluded from further analysis because of its un-well characterized nature). Genes with TPM higher than 2 were considered as detectable. The trans-spliced juntion mapped reads were quantified with a customized python script. Differential expression between each cancer types and healthy donors was performed using glmlrt method in edgeR package.

## Post-transcriptional modification analysis

  Here we use percentage spliced in (psi) value estimated by rMATs software as a surrogate for the relative abundance of differentially spliced isoforms. Differentially spliced genes were determined by rMAT's build in statistical testing methods. 
 Differential alternative polyadenylation analysis was performed using DaPar scripts with default parameter. 
 RNAEditor was utilized for RNA editing analysis. Due to the limited sequencing coverage, a considerable editing events can only be detected in few samples. To leverage the data sparsity, the average and maximum editing level in each genes were utilized as the measurement for editing level of each gene.

## Other RNA variation analysis
  Chimeric RNAs were detected by STAR-fusion with default parameters.
  Potential SNPs were called using GATK4 HaplotypeCaller. To retrive relatively informative SNPs, only the intersection between detected SNPs and COSMIC database were kept. Variants likely to be attribute to RNA editing (A to G, G to A, C to T or T to C conversion ) were filtered. Chimeric RNAs and SNVs that were only detected in one samples were thought to be noise, and excluded further analysis.


## Classification of unmapped reads

## Discovery-Validation Splitting
  Samples from healthy donors and patients with different cancer types were stratified according to sample sources (from which hospital), genders, ages and cancer subtypes, then split into two dataset in 1:1 manner.


