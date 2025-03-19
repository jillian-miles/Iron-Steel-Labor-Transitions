#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 11:54:33 2023

@author: jillianmiles
"""
import os
import pandas as pd




#COMPILE OUTPUTS
counties = ['AlleghenyPA', 'LowndesMS', 'WhitleyIN', 'MorganAL', 'DeKalbIN', "MontgomeryIN", 'MeadeKY SCALED', 'FultonOH SCALED', 'MahoningOH SCALED', 'DuvalFl SCALED', 'JeffersonOH SCALED', 'JeffersonAL SCALED', 'BAU Correct hopefully', 'San PatricioTX']

modeltype = ['Base_']#, 'SA-SR_','SA-DR_','SA-SRDR_']

# Initialize counter
counter = 1

# Iterate over each combination of county and modeltype
for county in counties:
    for mtype in modeltype:
        # Construct the file path
        file_path = f'/Users/jillianmiles/Documents/Academic/Research/Data/Best Results/{mtype}{county}NOCOKE.xlsx'

        # Check if the file exists
        if os.path.exists(file_path):
            # Read in the 'Supply Remaining' tab
            df = pd.read_excel(file_path, sheet_name='Supply Remaining')
            df2 = pd.read_excel(file_path, sheet_name='Demand Remaining')

           # Copy data into a dataframe
            col_name = f'{mtype}_{county}'
            if counter == 1:
                Compiled_Supply_Remaining = df.rename(columns={'Number of Workers': col_name})
                Compiled_Demand_Remaining = df2.rename(columns={'Number of Workers': col_name})
            else:
                Compiled_Supply_Remaining[col_name] = df['Number of Workers']
                Compiled_Demand_Remaining[col_name] = df['Number of Workers']


            # Increase the counter
            counter += 1

# Display the resulting dataframe
# print(Compiled_Supply_Remaining)
Compiled_Supply_Remaining.to_csv('/Users/jillianmiles/Documents/Academic/Research/Data/Better Results/CompSR.csv')



# File path

#BRING IN OUT OF INDUSTRY DATA
file_path = '/Users/jillianmiles/Documents/Academic/Research/Data/DCED Direct Pulls/Overarching Data/DCED Data-Selected/Occupations - 10 Counties.csv'

# Read CSV file into a dataframe
df = pd.read_csv(file_path)

# Filter rows where "County Name" is "Allegheny"
filtered_df = df[df['County Name'] == 'Allegheny']

# Specify the columns to keep
selected_columns = ['County Name', 'SOC', 'Description', '2018 Jobs', '2023 Jobs', '2018 - 2023 Openings',
                     'Avg. Annual Openings', '2018 - 2023 Replacement Jobs', 'Annual Replacement Jobs',
                     'Current Year Age 55-64', 'Current Year Age 65+']

# Create a new dataframe with the selected columns
occupation_result_df = filtered_df[selected_columns]

# Display the resulting dataframe
print(occupation_result_df)



#BRING IN SKA DATA
SKAsTables = '/Users/jillianmiles/Documents/Academic/Research/Data/Results I guess/Similarity Metric Calculations - All SOCs SKAs - Just Data.xlsx'
reader = pd.ExcelFile(SKAsTables)

# Get the names of all sheets in the Excel workbook
sheet_names = reader.sheet_names

SKAs = {}

# Iterate through each sheet and create dataframes
for sheet_name in sheet_names:
    # Read the current sheet as a dataframe
    placeholder_df = pd.read_excel(reader, sheet_name)
    
    # Save the dataframe using the sheet name as the variable name
    # Make sure the sheet name is a valid variable name by removing special characters
    variable_name = sheet_name.replace(' ', '_').replace('-', '_').replace('/', '_').replace('\\', '_')
    SKAs[variable_name] = placeholder_df
    
Abilities_Importance_df = SKAs['Abilities_Importance']
Abilities_Level_df = SKAs['Abilities_Level']
Knowledge_Importance_df = SKAs['Knowledge_Importance']
Knowledge_Level_df= SKAs['Knowledge_Level']
Skill_Importance_df = SKAs['Skill_Importance']
Skill_Level_df= SKAs['Skill_Level']

Abilities_Importance_df = SKAs['Abilities_Importance'].set_index('Unnamed: 0').rename_axis('SOC')
Abilities_Level_df = SKAs['Abilities_Level'].set_index('Unnamed: 0').rename_axis('SOC')
Knowledge_Importance_df = SKAs['Knowledge_Importance'].set_index('Unnamed: 0').rename_axis('SOC')
Knowledge_Level_df = SKAs['Knowledge_Level'].set_index('Unnamed: 0').rename_axis('SOC')
Skill_Importance_df = SKAs['Skill_Importance'].set_index('Unnamed: 0').rename_axis('SOC')
Skill_Level_df = SKAs['Skill_Level'].set_index('Unnamed: 0').rename_axis('SOC')


data_to_copy = {
    "11-3013": "11-1021",
    "11-9199": "11-3051",
    "13-1028": "13-1023",
    "13-1199": "13-1161",
    "13-1082": "13-1081",
    "13-2051": "11-3031",
    "15-1252": "15-1251",
    "17-3029": "17-3026",
    "41-3091": "41-1012",
    "51-2098": "51-2031",
    "51-4199": "51-4191",
    "51-9199": "51-9023",
    "53-1047": "53-1042"
}

for key, value in data_to_copy.items():
    Abilities_Importance_df.loc[key] = Abilities_Importance_df.loc[value]
    Abilities_Importance_df[key] = Abilities_Importance_df[value]
    Abilities_Level_df.loc[key] = Abilities_Level_df.loc[value]
    Abilities_Level_df[key] = Abilities_Level_df[value]
    Knowledge_Importance_df.loc[key] = Knowledge_Importance_df.loc[value]
    Knowledge_Importance_df[key] = Knowledge_Importance_df[value]
    Knowledge_Level_df.loc[key] = Knowledge_Level_df.loc[value]
    Knowledge_Level_df[key] = Knowledge_Level_df[value]
    Skill_Importance_df.loc[key] = Skill_Importance_df.loc[value]
    Skill_Importance_df[key] = Skill_Importance_df[value]
    Skill_Level_df.loc[key] = Skill_Level_df.loc[value]
    Skill_Level_df[key] = Skill_Level_df[value]



#BRING IN SALARY DATA
#import salary data
from uploadedSalary import Salary_data_df



# List of dataframes
dfs = [Abilities_Importance_df, Abilities_Level_df, Knowledge_Importance_df,
       Knowledge_Level_df, Skill_Importance_df, Skill_Level_df]

# Create OOI_Comparison dataframe with SOC as index and Abilities_Importance_df columns
OOI_Comparison = pd.DataFrame(index=Compiled_Supply_Remaining['SOC'],
                              columns=Abilities_Importance_df.columns)

# Loop through each row and column to compare values
for soc in Compiled_Supply_Remaining['SOC']:
    for col in Abilities_Importance_df.columns:
        values = [df.loc[soc, col] for df in dfs]
        median_values = [df[col].median() for df in dfs]
        
        # Check if all values are greater than the corresponding median values
        if all(value > median for value, median in zip(values, median_values)):
            OOI_Comparison.loc[soc, col] = "Y"
        else:
            OOI_Comparison.loc[soc, col] = "N"

# Print the resulting OOI_Comparison dataframe
print(OOI_Comparison)

# Create OOI_Comparison dataframe with SOC as index and Abilities_Importance_df columns
OOI_Comparison2 = pd.DataFrame(index=Compiled_Supply_Remaining['SOC'],
                              columns=Abilities_Importance_df.columns)

#UPDATE WITH CHRISTOPHE METHOD HERE ONCE WE HAVE TIME ENERGY AND PEACE OF MIND

for soc in Compiled_Supply_Remaining['SOC']:
    for salsoc in Salary_data_df.index:  # Use index directly
        valueA = Salary_data_df.loc[soc, 'Weighted Median Annual Earnings']
        valueB = Salary_data_df.loc[salsoc, 'Weighted Median Annual Earnings']
        
        if valueA >= valueB:
            OOI_Comparison2.loc[soc, salsoc] = "Y"
        else:
            OOI_Comparison2.loc[soc, salsoc] = "N"

print(OOI_Comparison2)


# Creating a new DataFrame as a copy of OOI_Comparison
new_df = OOI_Comparison.copy()

# Looping through rows and columns
for row in new_df.index:
    for col in new_df.columns:
        val1 = OOI_Comparison.at[row, col]
        val2 = OOI_Comparison2.at[row, col]

        if val1 == 'Y' and val2 == 'Y':
            new_df.at[row, col] = 'Y'
        elif val1 == 'Y' and val2 == 'N':
            new_df.at[row, col] = 'N: Sal'
        elif val1 == 'N' and val2 == 'Y':
            new_df.at[row, col] = 'N: SKA'
        elif val1 == 'N' and val2 == 'N':
            new_df.at[row, col] = 'N: Both'

# Displaying the new DataFrame
print(new_df)

new_df.to_csv('/Users/jillianmiles/Documents/Academic/Research/Data/Better Results/POSTPREP.csv')




'''
Make a new df that is a copy of OOI_Comparison
    for each row
        for each col
            check OOI_Comparison val there
            check OOI_Comparison2 val there
            if both "Y": 
                keep "Y"
            if OOI_Comparison is Y and OOI_Comparison2  is N
                change to "N: Sal"
            if OOI_Comparison is N and OOI_Comparison2  is Y
                change to "N: SKA"
            if both "N"
                change to "N: Both"

'''





'''
Make a new dataframe called OOI_Comparison with the rows being every SOC (column 1) in the Compiled_Supply_Remaining dataframe and the columns being the columns from the Abilities_Importance_df 
For every row:
    For every column:
        Find the associated row and column in these dataframes: 
            Abilities_Importance_df
            Abilities_Level_df
            Knowledge_Importance_df
            Knowledge_Level_df
            Skill_Importance_df
            Skill_Level_df
        Compare that value, to the median value of the column in the dataframes for each df.
        If the value is greater than the median value in all of the dfs:
            fill in the associated value in the OOI_Comparison with "Y"
        else:
            fill in the associated value in the OOI_Comparison with "N"




'''



'''

bring in the SKA tables 
And the salary values 

create 7 dfs (1 for each of them?)

Filter by 132 relevant SOC codes woo 

something about possible pathways !! Re-run

And then scale for the avg amount of openings in each occupation 



'''





'''
open /Users/jillianmiles/Documents/Academic/Research/Data/DCED Direct Pulls/Overarching Data/DCED Data-Selected/Occupations - 10 Counties.csv

I want the following from that file saved to a dataframe:
    only rows where the first column "County Name" is "Allegheny"
    and the following column values for each of those rows:
        County Name
        SOC
        Description
        2023 Jobs
        2018 - 2023 Openings
        Avg. Annual Openings
        2018 - 2023 Replacement Jobs
        Avg. Annual Replacement Jobs
        Current Year Age 55-64
        Current Year Age 65+




'''





'''

Open first file from  f'/Users/jillianmiles/Documents/Academic/Research/Data/Best Results/{modeltype}{counties}.xlsx'

[they are all excel files]


Read in the 'Suppy Remaining' tab. Copy data there into a dataframe called "Compiled Supply Remaining". Rename the third column title to be the part of the file name after  "Best Results" instead of "Number of Workers"
For the rest of the files in this folder, add a new column to the df and copy the data in the thrid column ("Number of Workers") into that new df column.
Name this columnd the same way as the other with that file name as the header. All of these files have the same first column (SOC) so they should all line up. 



# Look at all the occupations with positive growth rates

# Assess their salary and SKA transferabillity 

# Count out of how many in Allegheny Co. are growing, what the percentages of transferability are for each occupation

# from there, determine groups with lowest out-of-industry transferability, 



'''