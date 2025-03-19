#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 18:52:36 2023

@author: jillianmiles
"""


import pandas as pd
import numpy as np

#import list of employees
# and then a list of open jobs

from countylevelfiltering import sum_by_county_soc2

sum_by_county_soc = sum_by_county_soc2.reset_index()
# Get unique county names
unique_counties = sum_by_county_soc['County'].unique()


# Get unique county names
unique_counties = sum_by_county_soc['County'].unique()

# Create a dictionary to store individual DataFrames for each county
county_dfs = {}

# Iterate through unique counties
for county_name in unique_counties:
    # Filter data for the current county
    county_data = sum_by_county_soc[sum_by_county_soc['County'] == county_name].copy()
    
    # Store the result in the dictionary
    county_dfs[county_name] = county_data




def process_county(county_name):

    # Now you can access individual county DataFrames using their names
    # For example, to access the DataFrame for county 'Example County':
    county1_df = county_dfs['AlleghenyPA'].set_index('SOC')
    county2_df = county_dfs[county_name].set_index('SOC')
    
    supply_df = county1_df.copy()
    demand_df = county2_df.copy()
    
    supply_df['Number of Workers'] = supply_df['Number of Workers'].round().astype(int)
    demand_df['Number of Workers'] = demand_df['Number of Workers'].round().astype(int)
    
    all_indices = supply_df.index.union(demand_df.index)
    missing_in_supply = all_indices.difference(supply_df.index)
    missing_in_demand = all_indices.difference(demand_df.index)
    
    
    #import skills matrix
    #import knowledge matrix
    #import abilities matrix
    
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
    
    
    common_indices = supply_df.index.intersection(Abilities_Level_df.index)
    '''
    Abilities_Importance_df = Abilities_Importance_df.loc[common_indices]
    Abilities_Level_df = Abilities_Level_df.loc[common_indices]
    Knowledge_Importance_df = Knowledge_Importance_df.loc[common_indices]
    Knowledge_Level_df = Knowledge_Level_df.loc[common_indices]
    Skill_Importance_df = Skill_Importance_df.loc[common_indices]
    Skill_Level_df = Skill_Level_df.loc[common_indices]
    '''
    supply_df = supply_df.loc[common_indices]
    #demand_df = demand_df.loc[common_indices]
    
    
    #import salary data
    from uploadedSalary import Salary_data_df
    
    # create list of SOC codes from demand_df
    # look up 25 percentile salary for every job in the DemandD list
    
    
    job_ranks_supply = {}
    
    # Iterate through each SOC code in supply_df
    for soc_code in supply_df.index:
        # Look up the median salary for the current SOC code in Salary_data_df
        #print(type(median_salary))
        
        try:
            median_salary = Salary_data_df.loc[soc_code, 'Weighted Median Annual Earnings']
        except KeyError:
            print(f"Missing salary data for SOC code: {soc_code}")
            continue
        
        
        # Create a temporary list for jobs that meet the criteria
        temp_job_list = []
        
        try:
            median_skill = Skill_Importance_df.loc[soc_code].median()
            median_ability = Abilities_Importance_df.loc[soc_code].median()
            median_knowledge = Knowledge_Importance_df.loc[soc_code].median()
            
        except KeyError:
            print(f"Missing skills data for SOC code: {soc_code}")
            continue
        # Iterate through each job in Demand list
    
        for new_soc_code in demand_df.index:
            
            # IF AT lEAST 25 % of the PEOPLE MAKE AS MUCH AS I DO, 
            upper_quartile_sal = Salary_data_df.loc[new_soc_code, 'Weighted Pct. 75 Annual Earnings']
            if upper_quartile_sal >= median_salary:
                
                # and if job is at least in the similar half of jobs as me... 
                try: 
                    skill_importance = Skill_Importance_df.loc[soc_code, new_soc_code]
                    ability_importance = Abilities_Importance_df.loc[soc_code, new_soc_code]
                    knowledge_importance = Knowledge_Importance_df.loc[soc_code, new_soc_code]
                                    
                    if skill_importance >= median_skill and ability_importance >= median_ability and knowledge_importance >= median_knowledge:
                        combined_score = skill_importance + ability_importance + knowledge_importance
                        temp_job_list.append(new_soc_code)
    
                except KeyError:
                     #print(f"Missing skills data for SOC code: {new_soc_code}")
                     continue
                
        # Sort the remaining occupations based on salary (highest to lowest)
        sorted_jobs = sorted(
            temp_job_list,
            key=lambda x: Salary_data_df.loc[x, 'Weighted Pct. 75 Annual Earnings'],
            reverse=True
            )
    
        # Assign the sorted jobs to the dictionary with SOC code as key
        job_ranks_supply[soc_code] = sorted_jobs
    
    # Print the job ranks dictionary
    print("Job Ranks for Supply:")
    print(job_ranks_supply)
            
    
    # for each open job
        # any jobs that have median salary outside 90% range get nixed 
        # any jobs that don't meet median skill get nixed
        # any jobs that don't meet median ability get nixed
        # any jobs that don't meet median knowledge get nixed
        # rank based upon skill level
     
    job_ranks_demand = {}
    
    for soc_code in demand_df.index:
        try:
            new_ninety_salary = Salary_data_df.loc[soc_code, 'Weighted Pct. 90 Annual Earnings']
        except KeyError:
            print(f"Missing salary data for SOC code: {soc_code}")
            continue 
        try:
            median_skill = Skill_Level_df.loc[:,soc_code].median()
            median_ability = Abilities_Level_df.loc[:,soc_code].median()
            median_knowledge = Knowledge_Level_df.loc[:,soc_code].median()
        except KeyError:
            print(f"Missing skills data for SOC code: {soc_code}")
            continue
        
        temp_job_list2 = []
    
        for old_soc_code in supply_df.index:
            old_median_sal = Salary_data_df.loc[old_soc_code, 'Weighted Median Annual Earnings']
            if old_median_sal <= new_ninety_salary:
                try: 
                    skill_level = Skill_Level_df.loc[old_soc_code, soc_code]
                    ability_level = Abilities_Level_df.loc[old_soc_code, soc_code]
                    knowledge_level = Knowledge_Level_df.loc[old_soc_code, soc_code]
                    
                    if skill_level >= median_skill and ability_level >= median_ability and knowledge_level >= median_knowledge:
                        combined_score = skill_level + ability_level + knowledge_level
                        temp_job_list2.append((old_soc_code, combined_score))
                except KeyError:
                    #print(f"Missing skills data for SOC code: {old_soc_code}")
                    continue
            
        # Sort the remaining occupations based on the combined score (highest to lowest)
        sorted_jobs = sorted(
            temp_job_list2,
            key=lambda x: x[1],
            reverse=True
        )
    
        # Extract the sorted SOC codes from the sorted tuple list
        sorted_soc_codes = [soc for soc, _ in sorted_jobs]
    
        # Assign the sorted jobs to the dictionary with SOC code as key
        job_ranks_demand[soc_code] = sorted_soc_codes
    
    
    #make some dataframe that multiplies the two rankings together? 
    
    
    # create transition matrix that multiplies the the rankings together in a matrix
    
    # create a for loop that goes through the matrix and finds the lowest number and 
    
    
    # Create a supply-demand matrix with zeros
    supply_soc_codes = supply_df.index
    demand_soc_codes = demand_df.index
    
    # Create a supply-demand matrix with zeros and set SOC codes as column and row names
    matrix = np.zeros((len(supply_soc_codes), len(demand_soc_codes)), dtype=int)
    matrix = pd.DataFrame(matrix, index=supply_soc_codes, columns=demand_soc_codes)
    
    
    # Populate the matrix based on mutual inclusion in ranked lists
    for supply_idx, supply_code in enumerate(supply_soc_codes):
        if supply_code in job_ranks_supply:  # Make sure supply_code exists in job_ranks_supply
            for demand_idx, demand_code in enumerate(demand_soc_codes):
                if demand_code in job_ranks_demand:  # Make sure demand_code exists in job_ranks_demand
                    if demand_code in job_ranks_supply[supply_code] and supply_code in job_ranks_demand[demand_code]:
                        # Get the indices of demand_code in both lists and calculate the matrix value
                        supply_rank_idx = job_ranks_supply[supply_code].index(demand_code)+1
                        demand_rank_idx = job_ranks_demand[demand_code].index(supply_code)+1
                        matrix.loc[supply_code, demand_code] = supply_rank_idx + demand_rank_idx
    
    #print(matrix)
    matrix_initial = matrix.copy()
    
    
    # Initialize the transition matrix
    transition_matrix = np.zeros((len(supply_df), len(demand_df)), dtype=int)
    transition_matrix = pd.DataFrame(transition_matrix, index=supply_soc_codes, columns=demand_soc_codes)
    Unemployed_df = supply_df.copy()
    LaborShortage_df = demand_df.copy()
    
    def find_nonzero_indices(matrix):
        nonzero_indices = []
        for supply_idx, supply_code in enumerate(matrix.index):
            for demand_idx, demand_code in enumerate(matrix.columns):
                if matrix.iloc[supply_idx, demand_idx] != 0:
                    nonzero_indices.append((supply_code, demand_code))
        return nonzero_indices
    
    
    while True:
        # Find the indices of the minimum non-zero value in the matrix
        nonzero_indices = find_nonzero_indices(matrix)
        #print(nonzero_indices)
        
        if len(nonzero_indices) == 0:
            break
        
        # Find the minimum rank value in the remaining matrix
        min_rank = float('inf')
        for supply_code, demand_code in nonzero_indices:
            if matrix.loc[supply_code, demand_code] < min_rank:
                min_rank = matrix.loc[supply_code, demand_code]
        
        # Find all indices with the same minimum rank
        min_rank_indices = [(supply_code, demand_code) for supply_code, demand_code in nonzero_indices if matrix.loc[supply_code, demand_code] == min_rank]
        print(min_rank_indices)
            
        for idx in min_rank_indices:
            supply_code, demand_code = idx
            
            # Determine the available supply and demand counts
            available_supply = Unemployed_df.loc[supply_code, 'Number of Workers']
            available_demand = LaborShortage_df.loc[demand_code, 'Number of Workers']
            
            # Determine the matched count based on available supply and demand
            matched_count = min(available_supply, available_demand)
            
            # Update supply and demand counts
            Unemployed_df.loc[supply_code, 'Number of Workers'] -= matched_count
            LaborShortage_df.loc[demand_code, 'Number of Workers'] -= matched_count
            
            # Update the transition matrix
            transition_matrix.loc[supply_code, demand_code] += matched_count
            
            # Update the matrix
            matrix.loc[supply_code, demand_code] = 0
            
    
    
    print("Supply DataFrame after matching:")
    print(Unemployed_df)
    
    print("\nDemand DataFrame after matching:")
    print(LaborShortage_df)
    
    print("\nTransition Matrix:")
    print(transition_matrix)
    
    
    # Save the results with the county_name in the output file
    output_file = f'/Users/jillianmiles/Documents/Academic/Research/Data/Best Results/Base_{county_name}_NOCOKE.xlsx'

    with pd.ExcelWriter(output_file) as writer:
        # Saving dataframes to different tabs
        transition_matrix.to_excel(writer, sheet_name='Transition Matrix')
        Unemployed_df.to_excel(writer, sheet_name='Supply Remaining')
        LaborShortage_df.to_excel(writer, sheet_name='Demand Remaining')
        matrix_initial.to_excel(writer, sheet_name='Matrix - Inital Possible')


# Example usage:
counties_to_process = list(county_dfs.keys())

for county in counties_to_process:
    process_county(county)




'''

with pd.ExcelWriter('/Users/jillianmiles/Documents/Academic/Research/Data/Better Results/Possible Match with Ranks Matrix - Orig.xlsx') as writer:
    # Saving dataframes to different tabs
    matrix_initial.to_excel(writer, sheet_name='Matrix')
    '''

'''

def find_nonzero_indices(matrix):
    nonzero_indices = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 0:
                nonzero_indices.append((i, j))
    return nonzero_indices

def main():
    while True:
        # Find the indices of the minimum non-zero value in the matrix
        nonzero_indices = find_nonzero_indices(matrix)
        print(nonzero_indices)
        
        if len(nonzero_indices) == 0:
            break
        
        # Find the minimum rank value in the remaining matrix
        min_rank = float('inf')
        for i, j in nonzero_indices:
            if matrix[i][j] < min_rank:
                min_rank = matrix[i][j]
        
        # Find all indices with the same minimum rank
        min_rank_indices = [(i, j) for i, j in nonzero_indices if matrix[i][j] == min_rank]
        
        for idx in min_rank_indices:
            supply_idx, demand_idx = idx
            
            # Determine the available supply and demand counts
            available_supply = Unemployed_df.loc[supply_idx, 'Number of Workers']
            available_demand = LaborShortage_df.loc[demand_idx, 'Number of Workers']
            
            # Determine the matched count based on available supply and demand
            matched_count = min(available_supply, available_demand)
            
            # Update supply and demand counts
            Unemployed_df.loc[supply_idx, 'Number of Workers'] -= matched_count
            LaborShortage_df.loc[demand_idx, 'Number of Workers'] -= matched_count
            
            # Update the transition matrix
            transition_matrix[supply_idx][demand_idx] += matched_count
            
            # Update the matrix
            for i in range(len(matrix)):
                matrix[i][demand_idx] = 0
            for j in range(len(matrix[0])):
                matrix[supply_idx][j] = 0
    
    print("Supply DataFrame after matching:")
    print(Unemployed_df)
    
    print("\nDemand DataFrame after matching:")
    print(LaborShortage_df)
    
    print("\nTransition Matrix:")
    print(transition_matrix)

if __name__ == "__main__":
    main()







# Read data from Excel file
countysocdata = '/Users/jillianmiles/Documents/Academic/Research/Data/Results I guess/Sample Data.xlsx'
countysocdf = pd.read_excel(countysocdata )

# Iterate through the unique counties and create dataframes
for county in countysocdf['County'].unique():
    county_df = countysocdf[countysocdf['County'] == county].set_index('SOC')
    # Round the "Number of Workers" column to the nearest integer
    county_df['Number of Workers'] = county_df['Number of Workers'].round().astype(int)
    # Create a variable name using the county name (make sure the county name is a valid variable name)
    county_variable_name = county.replace(' ', '_') + '_df'
    # Assign the dataframe to the variable
    globals()[county_variable_name] = county_df
    # Print the dataframe
    print(f"DataFrame for {county} County:")
    print(county_df)
    print()
'''



