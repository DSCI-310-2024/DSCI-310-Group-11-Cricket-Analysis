import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import sklearn.metrics as metrics
from scripts.model_workflows import *

def test_split_train():
    data = pd.read_parquet('data/cricket_main.parquet')
    X = data.drop(columns = ['wicket'])
    y = data['wicket']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=123)

    X_train_output, X_test_output, y_train_output, y_test_output = split_train_test('data/cricket_main.parquet')

    assert(len(X_train) == len(X_train_output))
    assert(len(X_test) == len(X_test_output))
    assert(len(y_train) == len(y_train_output))
    assert(len(y_test) == len(y_test_output))

    assert((X_train.index == X_train_output.index).all())
    assert((X_test.index == X_test_output.index).all())
    assert((y_train.index == y_train_output.index).all())
    assert((X_train.index == X_train_output.index).all())


def test_preprocessing():
    ohe, scaler = preprocessing()
    params_ohe = ohe.get_params()
    params_scaler = scaler.get_params()
    ohe_test = OneHotEncoder(drop = "if_binary", handle_unknown="ignore").get_params()
    scaler_test = StandardScaler().get_params()

    assert(params_ohe["categories"] == ohe_test["categories"])
    assert(params_ohe["drop"] == ohe_test["drop"])
    assert(params_ohe["dtype"] == ohe_test["dtype"])
    assert(params_ohe["feature_name_combiner"] == ohe_test["feature_name_combiner"])
    assert(params_ohe["handle_unknown"] == ohe_test["handle_unknown"])
    assert(params_ohe["max_categories"] == ohe_test["max_categories"])
    assert(params_ohe["min_frequency"] == ohe_test["min_frequency"])
    assert(params_ohe["sparse_output"] == ohe_test["sparse_output"])

    assert(params_scaler["copy"] == scaler_test["copy"])
    assert(params_scaler["with_mean"] == scaler_test["with_mean"])
    assert(params_scaler["with_std"] == scaler_test["with_std"])


def test_transformer():
    ohe, scaler = preprocessing()
    ct = transformer(ohe, scaler)
    assert(ct.transformers[0][0] == "standardscaler")
    assert(ct.transformers[1][0] == "onehotencoder")
    assert(ct.transformers[2][0] == "drop")


def test_build_final_mode():
    ohe, scaler = preprocessing()
    ct = transformer(ohe, scaler)
    X_train, X_test, y_train, y_test = split_train_test('data/cricket_main.parquet')
    final_pipe = build_final_model(ct, X_train, y_train)

    assert(list(final_pipe.named_steps.keys())[0] == "columntransformer")
    assert(list(final_pipe.named_steps.keys())[1] == "logisticregression")

def test_evaluate_model():
    ohe, scaler = preprocessing()
    ct = transformer(ohe, scaler)
    X_train, X_test, y_train, y_test = split_train_test('data/cricket_main.parquet')
    final_pipe = build_final_model(ct, X_train, y_train)
    score, conf_mat, plot_cm = evaluate_model(final_pipe, X_test, y_test, "images/")

    assert(score == final_pipe.score(X_test, y_test))
    assert((conf_mat == metrics.confusion_matrix(y_test, final_pipe.predict(X_test))).all())
    assert(isinstance(plot_cm, metrics.ConfusionMatrixDisplay))
    





    














