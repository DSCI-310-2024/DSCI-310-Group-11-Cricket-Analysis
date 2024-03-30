import pandas as pd

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

