import numpy as np
import pandas as pd
import altair as alt
import os
import pytest
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.eda_functions import vis_bar
import helpers as hp

# test that df has the column
def test_vis_bar_column():
    assert hp.x_input1 in hp.data.columns,f"Column does not exist in the DataFrame."
    assert hp.x_input2 in hp.data.columns,f"Column does not exist in the DataFrame."

# test for correct input types
def test_vis_bar_input():
    assert isinstance(hp.data, pd.DataFrame), "Data is not a dataframe"
    assert isinstance(hp.x_input1, str), "Column is not a string"
    assert isinstance(hp.width1, int), "Width is not an integer"
    assert isinstance(hp.height1, int), "Height is not an integer"
    assert isinstance(hp.x_input2, str), "Column is not a string"

# test for correct outputs
def test_vis_bar_output():
    assert isinstance(hp.result1, alt.Chart), "Output is not an Altair Chart"
    assert isinstance(hp.result2, alt.Chart), "Output is not an Altair Chart"
    #assert hp.result1.encoding.x.field == x_input, "x_input should be the x axis"
    # assert vis_bar(data, x_input, width, height).encoding.y.field == 'count()', 'y axis should be count'
    # assert result.properties.width == width, "Width should be width specified"
    # assert vis_bar(data, x_input, width, height).properties.height == height, "height should be height specified"
