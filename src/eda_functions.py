import numpy as np
import pandas as pd
import altair as alt
import os
import click
import matplotlib.pyplot as plt


def vis_bar(data, x_input, width, height):
    """
    function to plot the distribution of variables in the dataset

    data: dataframe

    x_input: column for which the distribution is being plotted

    """

    # make sure width and height are correct input types
    if type(width) != int or type(height) != int:
        raise TypeError("Width and Height must be integers")
    
    # make sure column name is correct input type
    elif type(x_input) != str:
        raise TypeError("X input must be a string")
    
    # ensure dataframe is not empty
    elif data.empty == True:
        raise ValueError("DataFrame shouldn't be empty")
    
    # if column is nominal, we include :N at the end. ensure that the actual column name is in the dataframe
    elif x_input[-2:] == ':N' and x_input[:-2] not in data.columns:
        raise KeyError("Column must be in DataFrame")

    elif x_input[-2:] != ':N' and x_input not in data.columns:
        raise KeyError("Column must be in DataFrame")
    # create chart
    else:

        # transform nominal columns
        if x_input[-2:] == ':N':
            x_input = x_input[:-2]
            data[x_input] = data[x_input].astype(str)
        chart = alt.Chart(data).mark_bar().encode(
            x = x_input,
            y = "count()"
        ).properties(
            width = width, 
            height = height
        )
    return chart

    
def hist_chart(data, col, chart_name, save_path):
    """
    function to create and save distribution of wickets across different categories

    data: dataframe
    
    column: category

    chart_name: what to save the image as

    save_path: filepath for images 
    """
    # check for type of filepath/name
    if type(chart_name) != str or type(save_path) != str:
        raise TypeError("Chart name and file paths must be strings")
    
    # check for type of column name
    elif type(col) != str:
        raise TypeError("X input must be a string")
    
    # ensure dataframe is not empty
    elif data.empty == True:
        raise ValueError("DataFrame shouldn't be empty")
    
    # ensure dataframe contains the necessary columns
    elif col not in data.columns or 'wicket' not in data.columns:
        raise KeyError("Column must be in DataFrame")
    else:
        count_wicket = data.groupby(col)['wicket'].count()
        chart = count_wicket.plot(kind = 'bar', xlabel=f"{col}", ylabel="Wicket Count")
        fig = chart.get_figure()
        fig.savefig(os.path.join(save_path, chart_name))