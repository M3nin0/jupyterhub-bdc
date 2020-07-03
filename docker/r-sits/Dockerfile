# FROM jupyter/scipy-notebook:137a295ff71b
FROM jupyter/datascience-notebook

COPY env.R env.R

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \ 
    libudunits2-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID
RUN conda install --yes \
    'r-units' \
    'r-rgdal' \
    'r-sf'

RUN Rscript env.R
