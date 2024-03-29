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

# test for correct outputs
def test_vis_bar_output():
    assert isinstance(hp.result1, alt.Chart), "Output is not an Altair Chart"
    assert isinstance(hp.result2, alt.Chart), "Output is not an Altair Chart"

# test key error
def test_column_error():
    with pytest.raises(KeyError):
        vis_bar(hp.data1, hp.x_input2, hp.width1, hp.height1)

# test type error
def test_int_error():
    with pytest.raises(TypeError):       
        vis_bar(hp.data1, hp.x_input1, hp.width2, hp.height2)

# test value error
def test_value_error():
    with pytest.raises(ValueError):
        vis_bar(hp.data2, hp.x_input1, hp.width1, hp.height1)


