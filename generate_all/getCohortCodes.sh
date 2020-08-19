#!/bin/bash
#curl 'https://raw.githubusercontent.com/ucscXena/XenaGoWidget/develop/src/data/defaultDatasetForGeneset.json' | jq 'keys'  | cut -f2 -d '(' | cut -f1 -d ')' | grep -v "\[" | grep -v "\]" | grep -v Breast | tee  cohortCodes.txt

CODES=`cat cohortCodes.txt`

echo $CODES

for COHORT in $CODES
do
   echo "DOWNLOADING $COHORT"
   wget "https://xenago.xenahubs.net/download/expr_tpm/TCGA-${COHORT}_tpm_tab.tsv.gz"
done

gunzip *.gz

echo "ARGS: $1 $2"




for COHORT in $CODES
do
   echo "PROCESSING $COHORT"

#   wget "https://xenago.xenahubs.net/download/expr_tpm/TCGA-${COHORT}_tpm_tab.tsv.gz"

  Rscript ../analysis-wrapper.R $1 TCGA-${COHORT}_tpm_tab.tsv geneset_output_${COHORT}.tsv

   echo "DONE processing $COHORT -> ${geneset_output_${COHORT}.tsv}"
done
