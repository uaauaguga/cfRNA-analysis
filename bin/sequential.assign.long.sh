bam=$1
outputdir=$2
beddir=$3
regions=`cat config/priority.txt`
if [ ! -f ${outputdir}/sorted.reads.bed ];then
echo "Sorting bam file..."  > ${outputdir}/log.txt
samtools view -bf 0x2 ${bam} \
| bedtools bamtobed -bedpe -mate1 \
| awk 'BEGIN{{OFS="\t";FS="\t"}}{{print $1,$2,$3,$7,$8,$9; s=$10;if(s=="+"){{s="-"}}else if(s=="-"){{s="+"}}print $4,$5,$6,$7,$8,s}}' \
| /BioII/lulab_b/jinyunfan/software/bedops/bin/sort-bed - > ${outputdir}/sorted.reads.bed
echo "Done!"  >> ${outputdir}/log.txt
else
echo "Bam file already sorted!" >> ${outputdir}/log.txt
fi
regionalCounts=""
for region in ${regions}
do
regionalCounts="${regionalCounts} ${outputdir}/${region}.count.txt"
if [ ! -s ${outputdir}/${region}.count.txt ];then
echo "Counting ${region} ..." #>> ${outputdir}/log.txt
cat ${outputdir}/sorted.reads.bed \
| bedtools coverage -counts -S -sorted -a - -b ${beddir}/${region}.bed \
| sort -k 4 \
|awk 'BEGIN{{IFS="\t";OFS="\t";}}{{if(NR%2==1){{former=$7;}}else{{if(former>0||$7>0){{print 1;former=0;}}else{{print 0;former=0;}}}}}}'  > ${outputdir}/${region}.count.txt
echo "Done!" >> ${outputdir}/log.txt
else 
echo "${region} already counted!" >> ${outputdir}/log.txt
fi
done
paste ${regionalCounts} > ${outputdir}/result.txt
cat ${outputdir}/result.txt  | awk -v regions="${regions}" 'BEGIN{OFS="\t";split(regions,regionList," ");nRegions=length(regionList);for(i=1;i<=nRegions;i++){regionCounts[i]=0;}}{split($0,data," ");for(i=1;i<=nRegions;i++){if(data[i]>0){regionCounts[i]+=1;break;}}}END{for(i=1;i<=nRegions;i++){print regionList[i],regionCounts[i];}}' > ${outputdir}/counts.txt
