#!/bin/bash

CODES=`cat cohortCodes.txt`

echo $CODES

for COHORT in $CODES
do
   echo "DOWNLOADING $COHORT"
   wget "https://xena-go-data.s3.amazonaws.com/collated-genesets/collated-genesets-${COHORT}.tsv.gz"
done

gunzip *.gz

