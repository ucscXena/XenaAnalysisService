library(plumber)
r <- plumb("analysis-wrapper.R")  # Where 'plumber.R' is the location of the file shown above
r$run(port=8000)
