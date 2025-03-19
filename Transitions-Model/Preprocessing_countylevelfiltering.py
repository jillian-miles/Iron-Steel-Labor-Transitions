#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:24:28 2023

@author: jillianmiles
"""
import pandas as pd

# Define the list of counties
counties = ['AlleghenyPA', 'LowndesMS', 'WhitleyIN', 'MorganAL', 'DeKalbIN', "MontgomeryIN", 'MeadeKY SCALED', 'FultonOH SCALED', 'MahoningOH SCALED', 'DuvalFl SCALED', 'JeffersonOH SCALED', 'JeffersonAL SCALED', 'BAU Correct hopefully', 'San PatricioTX']

#['San PatricioTX',  'LowndesMS', 'WhitleyIN', 'St_LandryLA', 'MontgomeryIN', 'ButlerOH', 'DuvalFL', 'MorganAL', 'BerkeleySC', 'MississippiAR', 'DauphinPA', 'MadisonIL', 'JeffersonOH', 'DeKalbIN', 'LucasOH', 'LowndesMS', 'JeffersonAL', 'MahoningOH', 'San PatricioTX', 'FultonOH', 'MeadeKY']
#'DeKalbIN', 'LowndesMS', 'MontgomeryIN', 'MorganAL', 'ButlerPA' 'LucasOH'

#PA PA PA 'GreenePA', 'WestmorelandPA', 'ButlerPA', 'LawrencePA', 'WashingtonPA', 'FayettePA', 'ArmstrongPA', 'AlleghenyPA' 'BeaverPA', 'IndianaPA', 
#RIP WhitleyIN get outta here.... 

# Get NAICS code list
#from CleanedFilteringandSkills import Iron_Steel_NAICS

Iron_Steel_NAICS =  [324199, 331110]
#[331222, 331210, 324199, 331110, 331513, 331511, 332111, 331221, 331512]
 #[324199, 331110, 331111]

# Initialize an empty list to store all data frames
dfs = []

# For each county, load in data, and make a new data frame with just the required columns and filters
for county in counties:
    file_path = f'/Users/jillianmiles/Documents/Academic/Research/data/DCED Direct Pulls/County by County SOC NAICS Transposed-selected/{county} Staffing Patterns new.csv'
    df = pd.read_csv(file_path)
    
    # Filter the data to include only the desired NAICS codes
    df = df[df['NAICS'].isin(Iron_Steel_NAICS)]
    
    # Filter the data to include only rows with "Number of Workers" greater than 1
    df = df[df['Number of Workers'] > 1]
    
    # Create a new column for the county
    df['County'] = county
    
    # Reorder the columns to have "County", "NAICS", "SOC", and "Number of Workers" at the front
    df = df[['County', 'NAICS', 'SOC', 'Number of Workers']]
    
    # Append the filtered data frame to the list of data frames
    dfs.append(df)

# Combine all data frames into one by concatenating them vertically
combined_df = pd.concat(dfs, ignore_index=True)

# Calculate the sum of workers for each SOC

sum_by_soc = combined_df.groupby('SOC')['Number of Workers'].sum()

soc_codes_to_keep = sum_by_soc[sum_by_soc >= 1].index
combined_df = combined_df[combined_df['SOC'].isin(soc_codes_to_keep)]

# Now, the 'combined_df' contains the combined data from all counties with the desired filters and column order.
# You can save it to a new CSV file if needed:
# combined_df.to_csv('path/to/combined_data.csv', index=False)

sum_by_soc_new = combined_df.groupby('SOC')['Number of Workers'].sum()

# Calculate the sum of workers for each county
sum_by_county = combined_df.groupby('County')['Number of Workers'].sum()

# Calculate the sum of workers for each NAICS
sum_by_naics = combined_df.groupby('NAICS')['Number of Workers'].sum()

# Calculate the sum of workers for each county
sum_by_county_naics = combined_df.groupby(['County', 'NAICS'])['Number of Workers'].sum()

# Calculate the sum of workers for each county
sum_by_county_soc = combined_df.groupby(['County', 'SOC'])['Number of Workers'].sum()

# Calculate the sum of workers for each county
sum_by_naics_soc = combined_df.groupby(['NAICS', 'SOC'])['Number of Workers'].sum()

# All???? 
sum_by_all = combined_df.groupby(['County', 'NAICS', 'SOC'])['Number of Workers'].sum()

'''
# Filter out rows where NAICS code is 324199
combined_df2 = combined_df[combined_df['NAICS'] != 324199]

# Calculate the sum of workers for each county and SOC after filtering
sum_by_county_soc2 = combined_df2.groupby(['County', 'SOC'])['Number of Workers'].sum()

# Print the results
print("\nSum of workers by County and SOC:")
print(sum_by_county_soc2)

sum_by_all2 = combined_df2.groupby(['County', 'NAICS', 'SOC'])['Number of Workers'].sum()



print("Sum of workers by County:")
print(sum_by_county)
print("\nSum of workers by SOC:")
print(sum_by_soc)
print("\nSum of workers by NAICS:")
print(sum_by_naics)

matrix_county_naics = sum_by_county_naics.reset_index().pivot_table(index='County', columns='NAICS', values='Number of Workers', fill_value=0)
### FOR FULL PATHWAYS
soc_indices_list = sum_by_soc.index.tolist()


'''
