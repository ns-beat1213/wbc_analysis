# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 00:34:28 2023

@author: nsbea
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

path = 'C:/Users/nsbea/OneDrive/4_coding/wbc/data'
os.chdir(path)

# read dataset
df_itary = pd.read_csv('Itary/combined_file.csv')
df_japan = pd.read_csv('japan/combined_file.csv')

# numeric columns
num_col = ['Pitch Vel  (MPH)',
           'Spin (RPM)',
           'VBreak (In.)Vertical Break (Inches)',
           'HBreak (In.)Horizontal Break (Inches)',
           ]

# the columns used for analysis
col_name = ['date', 'country', 'vs', 'Pitcher', 'Batter', 'Game Pitch #',
            'Pitch', 'PA','Inning', 'Result', 'Pitch Type', 'Pitch Vel  (MPH)',
            'Spin (RPM)', 'VBreak', 'HBreak']

# to cleaning the data
def cleaning(df):
    # delete white space
    df[df.select_dtypes(include='object').columns] = df.select_dtypes(include='object').apply(lambda x: x.str.strip())
    
    # fill NaN
    df = df.replace('', np.nan)
    df = df.fillna(np.nan)
    
    # change object to numeric
    df[num_col] = df[num_col].apply(pd.to_numeric)
    
    # rename
    col_map = {'Unnamed: 14': 'up', 'Unnamed: 16': 'side'}
    df = df.rename(col_map, axis=1)
    
    # side map left means -1, right means 1
    side_map = {'←': -1, '→':1}
    df['side'] = df['side'].map(side_map)
    
    # define V/H break (the size of the change)
    df['VBreak'] = df['VBreak (In.)Vertical Break (Inches)'] *(-1)
    df['HBreak'] = df['HBreak (In.)Horizontal Break (Inches)'] * df['side']
    df['HBreak'] = df['HBreak'].replace(np.nan, 0)
    
    # delete unused columns
    df = df[col_name]
    return df

# sort pitcher data
pit_jp = ['Hiromi Itoh',
          'Atsuki Yuasa',
          'Shosei Togo',
          'Shohei Ohtani',
          'Hiroto Takahashi',
          'Yuki Matsui',
          'Yuki  Udagawa',
          'Shota Imanaga',
          'Yu Darvish',
          'Hiroya Miyagi',
          'Roki Sasaki',
          'Taisei Ota',
          'Keiji Takahashi',
          'Yoshinobu Yamamoto'
          ]

pit_itary = ['Mitchell Stumpo',
             'Matt Festa',
             'Joe LaSorsa',
             'Vinny Nittoli',
             'Andre Pallante',
             'Matt Harvey',
             'Claudio Scotti',
             'Joey Marciano',
             'Stephen Woods Jr.',
             'Joe Biagini',
             'Ryan Castellani',
             'Glenn Albanese Jr.',
             'Matteo Bocchi',
             'Sam Gaviglio',
             'Michele Vassalotti',
             ]

# cleaning
df_itary = cleaning(df_itary)
df_japan = cleaning(df_japan)

# delete unnecesary pitcher data
df_itary = df_itary[df_itary['Pitcher'].isin(pit_itary)]
df_japan = df_japan[df_japan['Pitcher'].isin(pit_jp)]


df = pd.concat([df_itary,df_japan], ignore_index=True)

df.to_csv('itary_japan.csv', index=False)


# visualization
# the columns used for analysis
col_name = ['date', 'country', 'vs', 'Pitcher', 'Batter', 'Game Pitch #',
            'Pitch', 'PA','Inning', 'Result', 'Pitch Type', 'Pitch Vel  (MPH)',
            'Spin (RPM)', 'VBreak', 'HBreak']

import seaborn as sns
df['Pitch Type'].unique()

major_type = ['4-Seam Fastball', 'Changeup', 'Cutter', 'Slider', 'Sinker']

major = df[df['Pitch Type'].isin(major_type)]

sns.boxplot(major, y= 'Pitch Type', x = 'Pitch Vel  (MPH)',hue='country')

jp_major = df_japan[df_japan['Pitch Type'].isin(major_type)]

sns.boxplot(df_japan, y= 'Pitcher', x = 'Spin (RPM)')

def plot_ind(name):
    temp = df_japan[df_japan['Pitcher'] == name]
    sns.scatterplot(temp, x= 'HBreak', y='VBreak', hue='Pitch Type')
    plt.plot()
    
plot_ind('Yu Darvish')
plot_ind('Shohei Ohtani')
