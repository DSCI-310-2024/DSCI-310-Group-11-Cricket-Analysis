import pandas as pd
import sys
import os
import pytest
from sklearn.model_selection import train_test_split

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_clean_functions import *
import helpers_data_clean as hp_dc


# Read the CSV file
@pytest.fixture
def dataframe():
    # Create or load your DataFrame here
    # For example:
    data = hp_dc.df_fake_test
    return data

@pytest.fixture
def caption():
    return "Table 0: test dataset"


# Drop the "Unnamed: 0" column
#data = data.drop(columns=["Unnamed: 0"])

# Verify that the "Unnamed: 0" column has been dropped
#assert "Unnamed: 0" not in data.columns, "Error: 'Unnamed: 0' column was not dropped."



def test_style_dataframe(dataframe, caption):
    styled_data = style_dataframe(dataframe, caption)

    # Verify that the DataFrame has been styled correctly
    assert styled_data is not None, "Error: DataFrame styling failed."

#   Test the functionality of the test_separate_columns function.
def test_separate_columns_function(dataframe):

    # Call the function being tested
    X, y = separate_columns(dataframe)

    # Check for the correct data types
    assert isinstance(X, pd.DataFrame), "Error: X should be a pandas DataFrame."
    assert isinstance(y, pd.Series), "Error: y should be a pandas Series."
    # Assert statements to check the functionality
    assert 'wicket' not in X.columns, "Error: 'wicket' column should be dropped from X."
    assert 'wicket' in y.name, "Error: 'wicket' column should be included in y."
    assert len(X) == len(y), "Error: Length of X and y should match."





def test_train_test_split_and_concat():

    X_train, X_test, y_train, y_test = train_test_split(hp_dc.X_fake, hp_dc.y_fake, train_size=0.7, shuffle=False)

    # Concatenate X_train and y_train to create the train_data DataFrame
    train_data = pd.concat([X_train, y_train], axis=1)

    # Step 3: Assertions
    # Assert that the shapes of X_train, X_test, y_train, and y_test are correct
    assert X_train.shape[0] == int(0.7 * hp_dc.X_fake.shape[0]), "Incorrect number of samples in X_train"
    assert X_test.shape[0] == hp_dc.X_fake.shape[0] - X_train.shape[0], "Incorrect number of samples in X_test"
    assert y_train.shape[0] == int(0.7 * hp_dc.y_fake.shape[0]), "Incorrect number of samples in y_train"
    assert y_test.shape[0] == hp_dc.y_fake.shape[0] - y_train.shape[0], "Incorrect number of samples in y_test"

    # Assert that train_data has the correct number of rows and columns
    assert train_data.shape[0] == X_train.shape[0], "Incorrect number of rows in train_data"
    assert train_data.shape[1] == X_train.shape[1] + 1, "Incorrect number of columns in train_data"

    # Assert that y column "wicket" is present in train_data
    assert 'wicket' in train_data.columns, "'wicket' column is missing in train_data"

    # Assert that X_train and X_train_fake are the same
    assert X_train.equals(hp_dc.X_train_fake), "X_train and X_train_fake are not the same"

    # Assert that X_test and X_test_fake are the same
    assert X_test.equals(hp_dc.X_test_fake), "X_test and X_test_fake are not the same"

    # Assert that y_train and y_train_fake are the same
    assert y_train.equals(hp_dc.y_train_fake), "y_train and y_train_fake are not the same"

    # Assert that y_test and y_test_fake are the same
    assert y_test.equals(hp_dc.y_test_fake), "y_test and y_test_fake are not the same"

  

