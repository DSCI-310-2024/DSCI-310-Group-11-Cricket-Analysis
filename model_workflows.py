import numpy as np
import pandas as pd
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

def split_data_from_parquet(parquet_path):
    data = pd.read_parquet(parquet_path)
    X = data.drop(columns = ['wicket'])
    y = data['wicket']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=123)
    return X_train, X_test, y_train, y_test


def save_training_data(X_train, y_train, save_path):
    train_data = pd.concat([X_train, y_train], axis = 1)
    train_data.to_csv(save_path, index=False)
    print(f"Training saved to: {save_file_path}")
    return train_data


def create_ct():
    """"
    Creates a Column Transformer 
    
    """
    ohe = OneHotEncoder(drop = "if_binary", handle_unknown="ignore")
    scaler = StandardScaler()

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


def tune_and_save_hyperparams(X_train, y_train, save_file_path):
    """"
    File path must include the ".csv" 
    
    """
    C = [10 ** x for x in [0.5, 1, 2, 3, 4]]
    train_score = []
    cv_score = []
    ct = create_ct()
    for c in C:
        model_new = LogisticRegression(C = c,  class_weight="balanced", n_jobs=-1)
        pipe_new = make_pipeline(ct, model_new)
        train_score.append(cross_validate(pipe_new, X_train, y_train, n_jobs =-1, return_train_score=True)['train_score'].mean())
        cv_score.append(cross_validate(pipe_new, X_train, y_train, n_jobs =-1, return_train_score=True)['test_score'].mean())
    results = pd.DataFrame({"C": C, "Training Accuracy": train_score, "Cross Validation Accuracy": cv_score})
    results.to_csv(save_file_path)
    return results

def prepare_chosen_model(X_train, y_train, C ):
    ct = create_ct()
    final_model = LogisticRegression(C, class_weight="balanced", n_jobs=-1)

    final_pipe = make_pipeline(
        ct,
        final_model
    )

    final_pipe.fit(X_train, y_train)

    return final_pipe


def evaluate_final_model(final_pipe, X_test, y_test, save_file_path):
    score = final_pipe.score(X_test, y_test)
    conf_mat = metrics.confusion_matrix(y_test, final_pipe.predict(X_test))
    plot_cm = metrics.ConfusionMatrixDisplay(conf_mat)
    plot_cm.plot()
    plt.savefig(save_file_path)
    print(f"Model Score: {score}")
    print(f"Chart saved to: {save_file_path}")









