# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 00:12:22 2023

@author: nsbea

for data cleaning
"""
import os
import pandas as pd
from datetime import datetime

date_format = '%Y%m%d'

# set function
def combine(file_paths, country):
    dfs = []
    for file_path in file_paths:
        df = pd.read_csv(file_path,header=1)
        df['date'] = datetime.strptime('2023'+str(file_path[0:4]), date_format)
        df['vs'] = file_path[5:-4]
        df['country'] = country
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    # save
    combined_df.to_csv('combined_file.csv', index=False)

# itary ---------------------------------------------------------------------------------
path = 'C:/Users/nsbea/OneDrive/4_coding/wbc/data/Itary'
os.chdir(path)
file_paths = ['0309_cuba.csv', '0310_chinesetaipei.csv', '0311_panama.csv', '0312_netherlands.csv']

combine(file_paths, 'Itary')

# Japan  --------------------------------------------------------------------------------
path = 'C:/Users/nsbea/OneDrive/4_coding/wbc/data/japan'
os.chdir(path)
file_paths = ['0309_China.csv', '0310_korea.csv', '0311_czech.csv', '0312_australia.csv']

combine(file_paths, 'Japan')



 