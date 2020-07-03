FROM jupyter/datascience-notebook

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \ 
    libudunits2-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY odc.sh odc.sh

RUN ./odc.sh

COPY .datacube.conf .datacube.conf
RUN chown $NB_UID:users .datacube.conf

RUN mkdir /gfs

USER $NB_UID

RUN conda install --yes nb_conda
