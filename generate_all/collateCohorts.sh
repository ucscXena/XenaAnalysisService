#!/bin/bash
#curl 'https://raw.githubusercontent.com/ucscXena/XenaGoWidget/develop/src/data/defaultDatasetForGeneset.json' | jq 'keys'  | cut -f2 -d '(' | cut -f1 -d ')' | grep -v "\[" | grep -v "\]" | grep -v Breast | tee  cohortCodes.txt

#echo "ARGS: $1 $2"
#
#if [ "$#" -ne 1 ]; then
#    echo "Illegal number of parameters $# not 1.  Usage: ./runAllCohorts <gmt_file>.tsv"
#	exit
#fi


CODES=`cat cohortCodes.txt`

echo $CODES

for COHORT in $CODES
do
   echo "COLLATE $COHORT"
#   wget "https://xenago.xenahubs.net/download/expr_tpm/TCGA-${COHORT}_tpm_tab.tsv.gz"
#   echo "Rscript ../analysis-wrapper.R  $1  TCGA-${COHORT}_tpm_tab.tsv $1-genesets-${COHORT}.tsv"
   #Rscript ../analysis-wrapper.R  $1  TCGA-${COHORT}_tpm_tab.tsv $1-genesets-${COHORT}.tsv
   #Rscript ../analysis-wrapper.R  $1  TCGA-${COHORT}_tpm_tab.tsv $1-genesets-${COHORT}.tsv
   head -1 h.all.v7.1.symbols.gmt-genesets-${COHORT}.tsv > collated-genesets-${COHORT}.tsv
   tail -n +2 h.all.v7.1.symbols.gmt-genesets-${COHORT}.tsv >> collated-genesets-${COHORT}.tsv
   
   tail -n +2 9606-bp-experimental.gmt_converted.tsv-genesets-${COHORT}.tsv | sed 's/ (GO:/-experimental_only (GO:/'>> collated-genesets-${COHORT}.tsv
   tail -n +2 9606-bp-computational.gmt_converted.tsv-genesets-${COHORT}.tsv| sed 's/ (GO:/-computational_only (GO:/' >> collated-genesets-${COHORT}.tsv
   tail -n +2 9606-bp-all.gmt_converted.tsv-genesets-${COHORT}.tsv >> collated-genesets-${COHORT}.tsv
#   9606-bp-computational.gmt_converted.tsv-genesets-${COHORT}.tsv
#   9606-bp-all.gmt_converted.tsv-genesets-${COHORT}.tsv
   #tail -n +1 *-genesets*${COHORT}.tsv h.all.v7.1.symbols.gmt-genesets-${COHORT}.tsv >> collated-genesets-${COHORT}.tsv
#   echo "GZIP $COHORT"
#   gzip collated-genesets-${COHORT}.tsv
#   echo "UPLOAD $COHORT"
#   aws s3 cp collated-genesets-${COHORT}.tsv.gz s3://xena-go-data/collated-genesets
done

#gunzip *.gz





#for COHORT in $CODES
#do
#   echo "PROCESSING $COHORT"

##   wget "https://xenago.xenahubs.net/download/expr_tpm/TCGA-${COHORT}_tpm_tab.tsv.gz"

#  Rscript ../analysis-wrapper.R $1 TCGA-${COHORT}_tpm_tab.tsv geneset_output_${COHORT}.tsv

#   echo "DONE processing $COHORT -> geneset_output_${COHORT}.tsv"
#done
