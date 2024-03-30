import numpy as np
import pandas as pd
import altair as alt
import os
import sys
import matplotlib.pyplot as plt



# Creating a dictionary with the data
data = {
    'game_id': ['1001349', '1001349', '1001350', '1001350', '1001351'],
    'season': ['2016/17', '2016/17', '2016/17', '2016/17', '2016/17'],
    'team': ['Australia', 'Australia', 'England', 'England', 'India'],
    'over': [0, 1, 0, 0, 1],
    'batter': ['AJ Finch', 'AJ Finch', 'JM Bairstow', 'JM Bairstow', 'V Kohli'],
    'batter_id': ['b8d490fd', 'b8d490fd', 'j4n5b78s', 'j4n5b78s', 'v7k3l9o2'],
    'bowler': ['SL Malinga', 'SL Malinga', 'C Woakes', 'C Woakes', 'JJ Bumrah'],
    'bowler_id': ['a12e1d51', 'a12e1d51', 'c7w4o2k5', 'c7w4o2k5', 'j5b2m3r4'],
    'non_striker': ['M Klinger', 'M Klinger', 'AD Hales', 'AD Hales', 'RG Sharma'],
    'non_striker_id': ['b970a03f', 'b970a03f', 'a1d4h89e', 'a1d4h89e', 'r8g3s5h2'],
    'wides': [0, 0, 1, 0, 1],
    'noballs': [0, 0, 1, 1, 0],
    'legbyes': [0, 1, 0, 0, 0],
    'byes': [1, 0, 0, 1, 1],
    'wicket': [0, 1, 0, 0, 0],
    'player_out': [None, None, None, None, None],
    'player_out_id': [None, None, None, None, None],
    'fielders_name': [None, None, None, None, None],
    'fielders_id': [None, None, None, None, None],
    'wicket_type': [None, None, None, None, None],
    'runs_batter': [0, 1, 0, 0, 0],
    'runs_extras': [1, 1, 0, 0, 1],
    'runs_total': [0, 0, 0, 1, 0],
    'team_over': ['Australia_0', 'Australia_0', 'England_0', 'England_0', 'India_0'],
    'over_ball': [1, 2, 3, 4, 5],
    'inning': [1, 1, 1, 1, 1],
    'runs_cumulative': [0, 1, 0, 1, 0],
    'powerplay': [0, 1, 0, 1, 0]
}

# Creating the DataFrame
df = pd.DataFrame(data)

# Displaying the DataFrame
print(df)