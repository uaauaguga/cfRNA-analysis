queue="Z-LU"
labels=metadata/covariates.txt
for data in editing splicing expression APA metagenomics ;do
input=variations/${data}.txt
outdir=output-0722-shuffle/${data}/CRC-STAD,LUAD,HCC,ESCA
[ -d ${outdir} ] || mkdir -p ${outdir}
bsub -q ${queue} "python  -W ignore bin/classification.py --input ${input} --labels ${labels} --pos CRC --neg STAD,LUAD,HCC,ESCA --model  ${outdir}/model.pickle --performance ${outdir}/performance.txt --roc ${outdir}/roc.txt --features ${outdir}/features.txt 2> log/${data}-CRC-OvR5-cancer-NC.txt"

outdir=output-0722-shuffle/${data}/STAD-LUAD,CRC,HCC,ESCA
[ -d ${outdir} ] || mkdir -p ${outdir}
bsub -q ${queue} "python  -W ignore bin/classification.py --input ${input} --labels ${labels} --pos STAD --neg CRC,LUAD,HCC,ESCA --model  ${outdir}/model.pickle --performance ${outdir}/performance.txt --roc ${outdir}/roc.txt --features ${outdir}/features.txt 2> log/${data}-STAD-OvR5-cancer-NC.txt"

outdir=output-0722-shuffle/${data}/HCC-STAD,LUAD,CRC,ESCA
[ -d ${outdir} ] || mkdir -p ${outdir}
bsub -q ${queue} "python  -W ignore bin/classification.py --input ${input} --labels ${labels} --pos HCC --neg STAD,LUAD,CRC,ESCA --model  ${outdir}/model.pickle --performance ${outdir}/performance.txt --roc ${outdir}/roc.txt --features ${outdir}/features.txt 2> log/${data}-HCC-OvR5-cancer-NC.txt"

outdir=output-0722-shuffle/${data}/LUAD-STAD,CRC,HCC,ESCA
[ -d ${outdir} ] || mkdir -p ${outdir}
bsub -q ${queue} "python  -W ignore bin/classification.py --input ${input} --labels ${labels} --pos LUAD --neg STAD,CRC,HCC,ESCA --model  ${outdir}/model.pickle --performance ${outdir}/performance.txt --roc ${outdir}/roc.txt --features ${outdir}/features.txt 2> log/${data}-OvR5-cancer-NC.txt"

outdir=output-0722-shuffle/${data}/ESCA-STAD,CRC,HCC,LUAD
[ -d ${outdir} ] || mkdir -p ${outdir}
bsub -q ${queue} "python  -W ignore bin/classification.py --input ${input} --labels ${labels} --pos ESCA --neg STAD,CRC,HCC,LUAD --model  ${outdir}/model.pickle --performance ${outdir}/performance.txt --roc ${outdir}/roc.txt --features ${outdir}/features.txt 2> log/${data}-ESCA-OvR5-cancer-NC.txt"
done
