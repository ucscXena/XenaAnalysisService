#!/bin/bash
curl 'https://raw.githubusercontent.com/ucscXena/XenaGoWidget/develop/src/data/defaultDatasetForGeneset.json' | jq 'keys'  | cut -f2 -d '(' | cut -f1 -d ')' | grep -v "\[" | grep -v "\]" | grep -v Breast > cohortCodes.txt


