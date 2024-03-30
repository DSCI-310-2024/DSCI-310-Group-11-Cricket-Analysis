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

@click.command()
@click.option('--parquet_path', type=str, help = 'File path of all data files', default='../data/cricket_main.parquet')
@click.option('--save_image_path', type=str, help = 'File path to save all images', default='../images')

def main(parquet_path, save_image_path):
    X_train, X_test, y_train, y_test = split_train_test(parquet_path)
    ohe, scaler = preprocessing()
    ct = transformer(ohe, scaler)
    final_pipe = build_final_model(ct, X_train, y_train)
    evaluate_model(final_pipe, X_test, y_test, save_image_path)

def split_train_test(parquet_path):
    data = pd.read_parquet(parquet_path)
    X = data.drop(columns = ['wicket'])
    y = data['wicket']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=123)
    return X_train, X_test, y_train, y_test

def preprocessing():
    ohe = OneHotEncoder(drop = "if_binary", handle_unknown="ignore")
    scaler = StandardScaler()
    return ohe, scaler

def transformer(ohe, scaler): 
    numerical_feats = ['runs_cumulative']
    categorical_feats = ['inning', 'over', 'powerplay', 'over_ball',]
    drop_feats = ['game_id', 'season', 'team','batter', 'batter_id', 'bowler',
        'bowler_id', 'non_striker', 'non_striker_id', 'wides', 'noballs',
        'legbyes', 'byes', 'player_out', 'player_out_id', 'fielders_name',
        'fielders_id', 'wicket_type', 'runs_batter', 'runs_extras', 
        'runs_total', 'team_over']
    
    ct = make_column_transformer(
        (scaler, numerical_feats), 
        (ohe, categorical_feats),
        ("drop", drop_feats)
    )

    return ct

def build_final_model(ct, X_train, y_train):
    final_model = LogisticRegression(class_weight="balanced", n_jobs=-1)

    final_pipe = make_pipeline(
        ct,
        final_model
    )
    final_pipe.fit(X_train, y_train)

    return final_pipe

def evaluate_model(final_pipe, X_test, y_test, save_image_path):
    score = final_pipe.score(X_test, y_test)
    conf_mat = metrics.confusion_matrix(y_test, final_pipe.predict(X_test))
    plot_cm = metrics.ConfusionMatrixDisplay(conf_mat)
    plot_cm.plot()
    plt.savefig(os.path.join(save_image_path, "chart7.png"))
    print(f"Model Score: {score}")
    print(f"Chart saved to: {save_image_path}")

    return score, conf_mat, plot_cm


if __name__ == '__main__':
    main()









