# FROM jupyter/scipy-notebook:137a295ff71b
FROM jupyter/datascience-notebook

COPY env.R env.R

USER root
RUN conda install -c conda-forge r-sf --yes
RUN conda install -c conda-forge proj-data --yes
RUN Rscript env.R

USER $NB_UID
