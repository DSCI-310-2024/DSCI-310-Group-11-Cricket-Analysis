import numpy as np
import pandas as pd
import altair as alt
import os
import pytest
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.eda_functions import vis_bar


# example inputs
data1 = pd.DataFrame({
    'A': [1, 0, 1],
    'B': [0, 1, 1],
    'C': [1, 1, 1]
})

data2 = pd.Series({})
data3 = pd.DataFrame({
    'A': ["hello", "goodbye"],
    'B': ["b", "a"]
})

x_input1 = 'A'
x_input2 = 'a'
width1 = 10
height1 = 20
width2 = "a"
height2 = 20.5

result1 = vis_bar(data1, x_input1, width1, height1)
result2 = alt.Chart()