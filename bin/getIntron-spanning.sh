#!/bin/bash
bam=$1
output=$2
(samtools view -H ${bam};
samtools view ${bam} |  \
awk 'BEGIN{is_first=1;}{ 
      split($0,fields,"\t"); 
      currentId=fields[1]; 
      if(formerId==currentId){is_first=0;} 
      if($6~/(.)+N(.)+/){flag=1;}else{flag=0;} 
      if(is_first==0){if(flag==1||former_flag==1){print former_line;print $0;}} 
      former_line=$0; 
      formerId=currentId; 
      former_flag=flag; 
      is_first=1; 
      } ' )| samtools view -b > ${output}
raw=$(samtools view ${bam} | wc -l)
filtered=$(samtools view ${output} | wc -l)
ratio=$(echo "scale=4;${filtered}/${raw}" | bc )
echo -e "raw\tfiltered\tratio"
echo -e "${raw}\t${filtered}\t${ratio}"


