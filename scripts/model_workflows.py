import numpy as np
import pandas as pd
import os
import click
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

from src.model_functions import *

@click.command()
@click.option('--parquet_path', type=str, help = 'File path of all data files', default='../data/cricket_main.parquet')
@click.option('--save_image_path', type=str, help = 'File path to save all images', default='../images')

def main(parquet_path, save_image_path):
    """
    the pipeline of building the model, where we split the data into train and test sets, 
    specify the preprocessors, add the preprocessors and the model into the pipe, evalute 
    the model. 
    """
    X_train, X_test, y_train, y_test = split_train_test(parquet_path)
    ohe, scaler = preprocessing()
    ct = transformer(ohe, scaler)
    final_pipe = build_final_model(ct, X_train, y_train)
    evaluate_model(final_pipe, X_test, y_test, save_image_path)

if __name__ == '__main__':
    main()









