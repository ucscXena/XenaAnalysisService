
FROM r-base
MAINTAINER Nathan Dunn <nathandunn@lbl.gov>
ENV DEBIAN_FRONTEND noninteractive

ADD . /
RUN Rscript install_packages_or_die.R BiocManager \
	Rscript install_packages_or_die.R plumber \
	Rscript install_packages_or_die.R viper \
	Rscript install_packages_or_die.R Rook \
	Rscript analysis-server.R

