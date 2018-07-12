#!/bin/bash
#$ -cwd
#$ -m as
#$ -M m.m.nieboer@umcutrecht.nl
#$ -pe threaded 12
#$ -l h_vmem=20G
#$ -l h_rt=60:00:00
#$ -e battenberg_e
#$ -o battenberg_o

#Running Battenberg

bamTumorFolder="$1"
outFolder="$2"
bamNormalFolder="$3"
baseDir="$4"

guixr environment --pure --ad-hoc cgp-battenberg r lsof -- << EOF

battenberg.pl -t 12 -outdir "$outFolder" -reference "$baseDir"/ref/hg19_noContig.fa.fai -tumbam "$bamTumorFolder"/sorted_chr.bam -normbam "$bamNormalFolder"/sorted_chr.bam -gender XX -impute-info "$baseDir"/battenbergData/impute/impute_info.txt -thousand-genomes-loc "$baseDir"/battenbergData/1000genomesloci/ -ignore-contigs-file "$baseDir"/battenbergData/ignore_contigs_file.txt

EOF



