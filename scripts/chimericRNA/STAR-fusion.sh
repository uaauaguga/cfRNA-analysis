#!/bin/bash
dataset=$1
STARdb=/Share2/home/lulab/jinyunfan/data/STAR-fusion-db/GRCh38_gencode_v31_CTAT_lib_Aug152019.plug-n-play/ctat_genome_lib_build_dir
sampleIDPath=data/${dataset}/sample_ids.txt
chimericDir=output/${dataset}/fusionGene
logDir=output/${dataset}/log/fusionGene
mkdir $chimericDir
mkdir $logDir
for sample_id in `cat ${sampleIDPath}`
do
outdir=${chimericDir}/${sample_id}
if [ ! -d $outdir ];then
mkdir $outdir
fi
fastqLeft=output/${dataset}/unmapped/${sample_id}/rRNA_1.fastq.gz
fastqRight=output/${dataset}/unmapped/${sample_id}/rRNA_2.fastq.gz
echo ${logDir}/${sample_id} $outdir
bsub -q Z-LU -n 6 -e ${logDir}/${sample_id}.err -o ${logDir}/${sample_id}.out -J ${sample_id}.fg "STAR-Fusion --CPU 6 --left_fq ${fastqLeft}  --right_fq ${fastqRight} --genome_lib_dir $STARdb --output_dir ${outdir}"
done
