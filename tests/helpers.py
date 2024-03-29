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
data = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})
x_input1 = 'A'
x_input2 = 'a'
width1 = 10
height1 = 20

result1 = vis_bar(data, x_input1, width1, height1)
result2 = vis_bar(data, x_input2, width1, height1)



