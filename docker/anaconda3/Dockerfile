FROM jupyter/datascience-notebook

USER root
RUN pip3 install wtss && pip3 install git+https://github.com/brazil-data-cube/stac.py@b-0.8.1

USER $NB_UID
