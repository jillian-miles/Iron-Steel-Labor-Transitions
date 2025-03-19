#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 13:57:54 2023

@author: jillianmiles
"""

#TRY THIS PLEASE


file_path1 = '/Users/jillianmiles/Documents/Academic/Research/Data/Better Results/POSTPREP75PERCENT.csv'

file_path2 = '/Users/jillianmiles/Documents/Academic/Research/Data/DCED Direct Pulls/Overarching Data/DCED Data-selected/Occupations - 10 Counties.csv'

import pandas as pd

occupation_result_df = pd.read_csv(file_path2)  
occupation_result_df = occupation_result_df[occupation_result_df["County Name"] == "Allegheny"]


# Read CSV file into a dataframe
postpret = pd.read_csv(file_path1, index_col=0)  # Assuming the first column is the index

# Create a new df that has the same indices as postpret and name it OOIA
OOIA = pd.DataFrame(index=postpret.index)

# Assuming you have a list of column names relevant to your DataFrame
relevant_columns = ['total_occupations_qualified_for','total_annual_openings', 'total_annual_replacement_jobs', 'total_annual_non_replacement_jobs']

# Create an empty DataFrame with the desired columns
OOIA = pd.DataFrame(0, index=OOIA.index, columns=relevant_columns)

# Iterate through rows and columns in postpret using iterrows()
for index, row in postpret.iterrows():
    # Initialize all relevant columns to be 0 for each row
    OOIA.loc[index, relevant_columns] = 0

    for col in postpret.columns:
            

        if row[col] == "Y":
            # Look up the row with that label in occupation_result_df
            print("yes")
            occupation_row = occupation_result_df.loc[occupation_result_df['SOC'] == col]

            # Check if occupation_row is not empty
            if not occupation_row.empty:
                # Add 1 to corresponding total annual openings col in OOIA
                OOIA.at[index, 'total_occupations_qualified_for'] += 1

                # Add the value for "Avg. Annual Openings" to annual openings col
                OOIA.at[index, 'total_annual_openings'] += occupation_row['Avg. Annual Openings'].values[0]

                # Add the value for "Annual Replacement Jobs" to annual replacement jobs col
                OOIA.at[index, 'total_annual_replacement_jobs'] += occupation_row['Annual Replacement Jobs'].values[0]

                # Add the value for "Annual Non-Replacement Jobs" to annual non-replacement jobs col
                # OOIA.at[index, 'total_annual_non_replacement_jobs'] += occupation_row['Annual Non-Replacement Jobs'].values[0]
            else:
                print(f"Warning: No data found for SOC {col}")

# Make the last col in OOIA equal to annual openings - annual replacement jobs
OOIA['total_annual_non_replacement_jobs'] = OOIA['total_annual_openings'] - OOIA['total_annual_replacement_jobs']

# Print the resulting dataframe
print(OOIA)
# Read CSV file into a dataframe
file_path3 = '/Users/jillianmiles/Documents/Academic/Research/Data/Better Results/CompSR.csv'
df3 = pd.read_csv(file_path3)

# Make a copy of the original OOIA dataframe
OOIApostdf = OOIA.copy()

# Average across only numeric columns for each row in df3
df3['AVG UNEMP'] = df3.select_dtypes(include='number').mean(axis=1)

# Merge 'AVG UNEMP' from df3 to OOIApostdf based on matching 'SOC' values
OOIApostdf = pd.merge(OOIApostdf, df3[['AVG UNEMP', 'SOC']], left_index=True, right_on='SOC', how='left')

# Drop the 'SOC' column from the result if not needed
#OOIApostdf = OOIApostdf.drop(columns='SOC')

# Calculate the new column "Ratio1"
OOIApostdf['Ratio1'] = OOIApostdf['total_annual_non_replacement_jobs'] - OOIApostdf['AVG UNEMP']

# Calculate the new column "Ratio2"
OOIApostdf['Ratio2'] = OOIApostdf['total_annual_non_replacement_jobs'] / OOIApostdf['AVG UNEMP']

OOIApostdf = OOIApostdf.set_index('SOC')


# Print the resulting dataframe
print(OOIApostdf)
OOIApostdf.to_csv('/Users/jillianmiles/Documents/Academic/Research/Data/Better Results/OOIAlooseResults75PERCENT.csv')

