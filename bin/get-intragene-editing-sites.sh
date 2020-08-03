#bedtools intersect -u -a recurrent-sites/recurrent-editing-sites-40-stranded.bed -b bed/gene.bed 
bedtools intersect -wa -wb -a recurrent-sites/recurrent-editing-sites-40-stranded.bed -b bed/gene.bed | sort-bed - | awk 'BEGIN{OFS="\t";}$6==$12{print $1"|"$3,$10}'
