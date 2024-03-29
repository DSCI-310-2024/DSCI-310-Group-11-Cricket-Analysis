import numpy as np
import pandas as pd
import altair as alt
import os
import click
import matplotlib.pyplot as plt


def vis_bar(data, x_input, width, height):
    if type(width) != int or type(height) != int:
        raise TypeError("Width and Height must be integers")
    elif data.empty == True:
        raise ValueError("DataFrame shouldn't be empty")
    elif x_input not in data.columns:
        raise KeyError("Column must be in DataFrame")
    else:
        chart = alt.Chart(data).mark_bar().encode(
            x = x_input,
            y = "count()"
        ).properties(
            width = width, 
            height = height
        )
    return chart
