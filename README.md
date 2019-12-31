# cfRNA-analysis
## Reads Preprocessing

  Adapter sequences in the raw sequencing data were removed using cutadapt with parameter -q 30,30 AGATCGGAAGAGCACACGTCTGAACTCCAGTCA   AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT --trim-n -m 30. The template switch oligo (TSO) sequences were then trimmed with a customized python script, reads shorter than 30 nt were discarded. The remaining reads were mapped to spike-in library, NCBI's UniVec Core sequences, human rRNA sequences with STAR aligner sequentially. 

## Quality Control and Transcriptome Quantification

  We used STAR aligner to map cleaned reads to hg38 genome index build with gencodev27 splice junction annotation. The unmapped reads were aligned to  sequence around junction site annotated in circBase (upstream 300 nt and downstream 300 nt). Duplications in genome and circular RNA mapped reads were removed using picard tools MarkDuplicates. 

 For quality control, genome mapped reads were sequentially assigned to one of the following genomic regions: lncRNA, mRNA, tucpRNA, srpRNA, snRNA, snoRNA, YRNA, other exon regions, intron, antisense, promoter, enhancer, and repeats. Here we use mitranscriptome annotation to define the genomic regions correspond to lncRNA and tucpRNA; regions of mRNA, srpRNA, snRNA, snoRNA and YRNA were specified accoding to gencodev27 annotation. Antisense RNA is defined as the reverse strand of exon regions. Repeat regions were download from UCSC GenomeBrowser. Promoter and enhancer regions were retrived from Broad ChromHMM annotations. 
  Genome mapped reads were quantified with featurecostoCounts, using mRNA,YRNA,snoRNA,snRNA srpRNA annotation in genecode v27, and lncRNA annotation in mitranscriptome . Genes with TPM higher than 2 were considered as detectable.  Mitochondrial  RNA, which makes up to 10% of total mRNAs, were excluded from differential expression analysis to reduce the noise. Genes that are undetectable in all of the six sample classes (CRC,GC,LC,EC,HCC and HD) were filtered. Differential expression between each cancer types and healthy donors was performed using glmlrt method in edgeR package. 

## Post-transcriptional Modification Analysis

 Percentage spliced in (psi) value estimated by rMATs software was utilized as a surrogate for the relative abundance of different isoforms. Differential alternative splicing events were determined by rMATs' build-in statistical testing methods with cut off FDR<0.05, Δpsi > 0.05. 
 Differential alternative polyadenylation analysis was performed using DaPar scripts with default parameter. APA events with adjusted p value lower than 0.05 were considered as different between two groups.
 RNA editing events were determined use RNAEditor software. Editing sites detected in more than 10% of the samples were retained. In each sample, editing sites with coverage higher than 3 were thought to be informative. We performed rank-sum test (ranksums in scipy package) for editing levels of editing sites with at least 3 informative samples in both classes. The resulting p value were adjusted by Benjamini-Hochberg FDR correction (multipletests function in statsmodels package). 

## Other RNA Variation Analysis
  Chimeric RNAs were detected by STAR-fusion with default parameters. Potential SNVs were called using GATK4 HaplotypeCaller.  Variants that could be attributed to RNA editing (A to G, G to A, C to T or T to C conversions ) were filtered. Chimeric RNAs and SNVs that were only detected in one sample were excluded.  Chimeric RNAs and SNVs with different frequency between cancer and healthy populations were identified using fisher exact test (fisher_exact function in scipy package) followed by Benjamini-Hochberg correction.


