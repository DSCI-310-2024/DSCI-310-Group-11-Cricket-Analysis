FROM quay.io/jupyter/scipy-notebook:2024-02-24

RUN conda install -y \
    jupyterlab=4.1.4 \
    python=3.11 \
    numpy=1.26.4 \
    pyarrow=15.0.1 \
    matplotlib=3.8.3 \
    pandas=2.2.1 \
    click=8.1.7 \
    scikit-learn=1.2.0 \
    altair=5.2.0 \
    vegafusion=1.6.5 \
    vl-convert-python=1.2.3 \
    pytest=8.1.1\
    make=4.3\
    quarto=1.4.550\
    pytest-cov=5.0.0\


