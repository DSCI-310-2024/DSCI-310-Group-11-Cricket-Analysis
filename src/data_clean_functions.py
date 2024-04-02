import pandas as pd
import os
from sklearn.model_selection import train_test_split

def style_dataframe(dataframe, caption):
    """
    Apply styling to a DataFrame.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to style.
        caption (str): The caption to add to the DataFrame.

    Returns:
        pd.io.formats.style.Styler: The styled DataFrame.
        
    Raises:
        TypeError: If dataframe is not a pandas DataFrame or if caption is not a string.
        ValueError: If the dataframe is empty.
    """
    # Check if dataframe is a pandas DataFrame
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas DataFrame")
    
    # Check if caption is a string
    if not isinstance(caption, str):
        raise TypeError("caption must be a string")
    
    # Check if dataframe is empty
    if dataframe.empty:
        raise ValueError("dataframe should not be empty")
    
    # Apply styling
    styled_data = dataframe.head().style.set_caption(caption).set_table_styles([{
        'selector': 'caption',
        'props': 'caption-side: bottom; font-size:1.25em;'
    }], overwrite=False)
    
    return styled_data



def separate_columns(dataframe):
    """
    Drop the 'wicket' column from the DataFrame and separate it as the target variable.

    Parameters:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        X (pd.DataFrame): DataFrame with the 'wicket' column dropped.
        y (pd.Series): Series containing the 'wicket' column (target variable).

    Raises:
        TypeError: If data is not a pandas DataFrame or if 'wicket' column is not present.
    """
    # Check if data is a pandas DataFrame
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame")

    # Check if 'wicket' column is present
    if 'wicket' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'wicket' column")

    # Drop the 'wicket' column from the DataFrame
    X  = dataframe.drop(columns=['wicket'])
    
    # Separate 'wicket' column as the target variable
    y = dataframe['wicket']

    return X, y



def split_and_save_data(X, y, train_size=0.7, save_table_path="."):
    """
    Split the data into training and testing sets, and save the training data to a CSV file.

    Parameters:
        X (pd.DataFrame): The features DataFrame.
        y (pd.Series): The target variable Series.
        train_size (float): The proportion of the dataset to include in the training set.
        random_state (int or None): Random seed for reproducibility.
        save_table_path (str): The path to save the CSV file.

    Returns:
        None

    Raises:
        TypeError: If X is not a pandas DataFrame, y is not a pandas Series, or save_table_path is not a string.
        ValueError: If train_size is not between 0 and 1.
        IOError: If there is an issue saving the CSV file.
    """
    # Check if X is a pandas DataFrame
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame")
    
    # Check if y is a pandas Series or DataFrame
    if not isinstance(y, (pd.DataFrame, pd.Series)):
        raise TypeError("y must be a pandas DataFrame or Series")
    
    # Check if train_size is between 0 and 1
    if not 0 < train_size < 1:
        raise ValueError("train_size must be a float between 0 and 1")

    # Check if save_table_path is a string
    if not isinstance(save_table_path, str):
        raise TypeError("save_table_path must be a string")

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size, shuffle=False,)
    
    # Concatenate X_train and y_train
    train_data = pd.concat([X_train, y_train], axis=1)

    # Save the training data to a CSV file
    try:
        train_data.to_csv(os.path.join(save_table_path, "train_data.csv"), index=False)
    except IOError as e:
        # Handle IOError
        print("Error occurred while saving the CSV file:", e)
    
    return X_train, X_test, y_train, y_test, train_data
