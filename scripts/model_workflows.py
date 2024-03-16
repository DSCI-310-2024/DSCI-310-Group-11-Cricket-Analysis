import numpy as np
import pandas as pd
import os
import click
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

@click.command()
@click.option('--parquet_path', type=str, help = 'File path of all data files', default='../data/cricket_main.parquet')
@click.option('--save_image_path', type=str, help = 'File path to save all images', default='../images')
@click.option('--save_table_path', type=str, help = 'File path to save all tables',default='../data/data_for_quarto')

def main(parquet_path, save_image_path, save_table_path):
    data = pd.read_parquet(parquet_path)
    X = data.drop(columns = ['wicket'])
    y = data['wicket']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=123)



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

    C = [10 ** x for x in [0.5, 1, 2, 3, 4]]
    train_score = []
    cv_score = []
    for c in C:
        model_new = LogisticRegression(C = c,  class_weight="balanced", n_jobs=-1)
        pipe_new = make_pipeline(ct, model_new)
        train_score.append(cross_validate(pipe_new, X_train, y_train, n_jobs =-1, return_train_score=True)['train_score'].mean())
        cv_score.append(cross_validate(pipe_new, X_train, y_train, n_jobs =-1, return_train_score=True)['test_score'].mean())
    results = pd.DataFrame({"C": C, "Training Accuracy": train_score, "Cross Validation Accuracy": cv_score})
    results.to_csv(os.path.join(save_table_path, "Hyperparameter.csv"))


    results['Difference'] = results['Training Accuracy'] - results['Cross Validation Accuracy']

    least_overfit = results.loc[results['Difference'] > 0, 'Difference'].min()
    index_best_C = results.index[results['Difference'] == least_overfit].tolist()[0]
    best_C = results.at[index_best_C, 'C']
    final_model = LogisticRegression(C = best_C, class_weight="balanced", n_jobs=-1)

    final_pipe = make_pipeline(
        ct,
        final_model
    )
    final_pipe.fit(X_train, y_train)
    score = final_pipe.score(X_test, y_test)
    conf_mat = metrics.confusion_matrix(y_test, final_pipe.predict(X_test))
    plot_cm = metrics.ConfusionMatrixDisplay(conf_mat)
    plot_cm.plot()
    plt.savefig(os.path.join(save_image_path, "chart7.png"))
    print(f"Model Score: {score}")
    print(f"Chart saved to: {save_image_path}")

if __name__ == '__main__':
    main()









