FROM quay.io/jupyter/scipy-notebook:2024-02-24

RUN conda install -y \
    jupyterlab=4.1.4 \
    python=3.11 \
    matplotlib=3.8.3 \
    pandas=2.2.1 \
    scikit-learn=1.2.0 \
    altair=5.2.0 \
    vegafusion=1.6.5 \
    vl-convert-python=1.2.3 


