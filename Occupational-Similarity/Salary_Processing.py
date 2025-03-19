#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 11:13:45 2023

@author: jillianmiles
"""

#retreiving other occupational data!!! 

import pandas as pd

def calculate_weighted_average(csv_file):
    df = pd.read_csv(csv_file)

    # Calculate weighted values
    df['Weighted Median Annual Earnings'] = df['Median Annual Earnings'] * df['2023 Jobs']
    df['Weighted Pct. 10 Annual Earnings'] = df['Pct. 10 Annual Earnings'] * df['2023 Jobs']
    df['Weighted Pct. 25 Annual Earnings'] = df['Pct. 25 Annual Earnings'] * df['2023 Jobs']
    df['Weighted Pct. 75 Annual Earnings'] = df['Pct. 75 Annual Earnings'] * df['2023 Jobs']
    df['Weighted Pct. 90 Annual Earnings'] = df['Pct. 90 Annual Earnings'] * df['2023 Jobs']
    df['Weighted Mean Annual Earnings'] = df['Avg. Annual Earnings'] * df['2023 Jobs']
    
    # Group by SOC code and calculate weighted averages
    grouped_df = df.groupby('SOC').agg({
        '2018 Jobs': 'sum',
        '2023 Jobs': 'sum',
        'Weighted Median Annual Earnings': 'sum',
        'Weighted Pct. 10 Annual Earnings': 'sum',
        'Weighted Pct. 25 Annual Earnings': 'sum',
        'Weighted Pct. 75 Annual Earnings': 'sum',
        'Weighted Pct. 90 Annual Earnings': 'sum',
        'Weighted Mean Annual Earnings': 'sum'
    })
    grouped_df['Weighted Median Annual Earnings'] = grouped_df['Weighted Median Annual Earnings'] / grouped_df['2023 Jobs']
    grouped_df['Weighted Pct. 10 Annual Earnings'] = grouped_df['Weighted Pct. 10 Annual Earnings'] / grouped_df['2023 Jobs']
    grouped_df['Weighted Pct. 25 Annual Earnings'] = grouped_df['Weighted Pct. 25 Annual Earnings'] / grouped_df['2023 Jobs']
    grouped_df['Weighted Pct. 75 Annual Earnings'] = grouped_df['Weighted Pct. 75 Annual Earnings'] / grouped_df['2023 Jobs']
    grouped_df['Weighted Pct. 90 Annual Earnings'] = grouped_df['Weighted Pct. 90 Annual Earnings'] / grouped_df['2023 Jobs']
    grouped_df['Weighted Mean Annual Earnings'] = grouped_df['Weighted Mean Annual Earnings'] / grouped_df['2023 Jobs']
    
    return grouped_df[[
        '2018 Jobs',
        '2023 Jobs',
        'Weighted Median Annual Earnings',
        'Weighted Pct. 10 Annual Earnings',
        'Weighted Pct. 25 Annual Earnings',
        'Weighted Pct. 75 Annual Earnings',
        'Weighted Pct. 90 Annual Earnings',
        'Weighted Mean Annual Earnings'
    ]]

csv_file = '/Users/jillianmiles/Documents/Academic/Research/data/DCED Direct Pulls/Overarching Data/DCED Data-selected/Occupations - 10 Counties.csv'

Salary_data_df = calculate_weighted_average(csv_file)

print(Salary_data_df)
