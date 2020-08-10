# XenaAnalysisService


### Analysis 


    Rscript transform_tpm_to_gene_set_activity.R ./Xena_manual_pathways.gmt ./TCGA-CHOL_logtpm_forTesting.tsv ./test_outfile.tsv BPA




### Web Server

Uses plumber: https://www.rplumber.io/  

    install.packages("plumber")
   
Run server:

    Rscript server.R
   
Test:

    curl "http://localhost:8000/echo
    curl "http://localhost:8000/echo?msg=hello
    curl --data "a=4&b=3" "http://localhost:8000/sum"
    curl --data '{"a":4, "b":5}' http://localhost:8000/sum
   


