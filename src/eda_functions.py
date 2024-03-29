import numpy as np
import pandas as pd
import altair as alt
import os
import click
import matplotlib.pyplot as plt


def vis_bar(data, x_input, width, height):
    chart = alt.Chart(data).mark_bar().encode(
        x = x_input,
        y = "count()"
    ).properties(
        width = width, 
        height = height
    )
    return chart

def write_caption(tbl_name, caption):
    tbl_name.style.set_caption(caption).set_table_styles([{
        'selector': 'caption',
        'props': 'caption-side: bottom; font-size:1.25em;'
    }], overwrite=False)
