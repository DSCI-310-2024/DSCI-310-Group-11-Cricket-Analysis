import numpy as np
import pandas as pd
import altair as alt
import os 
import pytest
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.eda_functions import *
import helpers_eda as hp

# test for correct vis_bar outputs
def test_vis_bar_output():
    assert isinstance(hp.result1, alt.Chart), "Output is not an Altair Chart"
    assert hp.result1.encoding.x.shorthand == hp.x_input1, "X-axis is not x-axis input"
    assert hp.result3.encoding.x.shorthand + ":N" == hp.x_input4, "X-axis is not x-axis input"
    assert hp.result1.encoding.y.shorthand == 'count()', "X-axis is not x-axis input"
    assert hp.result1.width == hp.width1, "Width is not width specified"
    assert hp.result1.height == hp.height1, "Height is not height specified"

# test for correct histogram outputs
def test_hist_output():
    assert os.path.isfile("images/Chart1.png"), "Image is not saved"

# test key error
def test_column_error():
    with pytest.raises(KeyError):
        vis_bar(hp.data1, hp.x_input2, hp.width1, hp.height1)

def test_wicket_error():
    with pytest.raises(KeyError):
        hist_chart(hp.data3, hp.x_input1, hp.chart1, hp.filepath1)

# test type error
def test_int_error():
    with pytest.raises(TypeError):       
        vis_bar(hp.data1, hp.x_input1, hp.width2, hp.height2)

def test_str_error():
    with pytest.raises(TypeError):
        vis_bar(hp.data1, hp.x_input3, hp.width1, hp.height1)

def test_his_col_error():
    with pytest.raises(TypeError):
        hist_chart(hp.data1, hp.x_input2, hp.chart2, hp.filepath2)

def test_filepath_error():
    with pytest.raises(TypeError):
        hist_chart(hp.data1, hp.x_input1, hp.chart2, hp.filepath2)
        
# test value error
def test_value_error():
    with pytest.raises(ValueError):
        vis_bar(hp.data2, hp.x_input1, hp.width1, hp.height1)


