import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

def split_train_test(parquet_path):
    """
    Read data from the provided path, exclude the 'wicket' column, 
    partition the data into training and testing sets with a 7:3 ratio, 
    specify the random state, and then return the resulting training and testing sets.
    """
    data = pd.read_parquet(parquet_path)
    X = data.drop(columns = ['wicket'])
    y = data['wicket']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=123)
    return X_train, X_test, y_train, y_test

def preprocessing():
    """
    Specify and return the preprocessors
    """
    ohe = OneHotEncoder(drop = "if_binary", handle_unknown="ignore")
    scaler = StandardScaler()
    return ohe, scaler

def transformer(ohe, scaler): 
    """
    Assign the relevant features to the preprocessors within the transformer and provide the resulting transformer.
    """
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
    """
    Combine the model with the transformer in the pipeline, 
    train the pipeline with the training set, and return the trained pipeline.
    """
    final_model = LogisticRegression(class_weight="balanced", n_jobs=-1)

    final_pipe = make_pipeline(
        ct,
        final_model
    )
    final_pipe.fit(X_train, y_train)

    return final_pipe

def evaluate_model(final_pipe, X_test, y_test, save_image_path):
    """
    Evaluate the model by generating the test score of the final pipeline. 
    Additionally, create the confusion matrix of the model and save it to the specified input path.
    """
    score = final_pipe.score(X_test, y_test)
    conf_mat = metrics.confusion_matrix(y_test, final_pipe.predict(X_test))
    plot_cm = metrics.ConfusionMatrixDisplay(conf_mat)
    plot_cm.plot()
    plt.savefig(os.path.join(save_image_path, "chart7.png"))
    print(f"Model Score: {score}")
    print(f"Chart saved to: {save_image_path}")

    return score, conf_mat, plot_cm
