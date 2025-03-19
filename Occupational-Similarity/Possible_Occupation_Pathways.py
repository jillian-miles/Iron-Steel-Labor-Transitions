#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 11:17:54 2023

@author: jillianmiles
"""
import pandas as pd
from uploadedSalary import Salary_data_df
from countylevelfiltering import soc_indices_list

IS_SOClist = soc_indices_list
#from similaritycalc3 import Skills_level_similarity_matrix, Abilities_level_similarity_matrix, Knowledge_level_similarity_matrix, knowledge_similarity_df, skills_similarity_df, abilities_similarity_df

#this file has the results from similarity run 4. 
excel_file = '/Users/jillianmiles/Documents/Academic/Research/data/Results I guess/Similarity Metric Calculations - All SOCs SKAs.xlsx'

# Read all sheets from the Excel file into a dictionary of DataFrames
dataframes_dict = pd.read_excel(excel_file, sheet_name=None, index_col=0)

# Print all sheet names
print("Sheet names in the Excel file:")
for sheet_name in dataframes_dict.keys():
    print(sheet_name)


#IS_SOClist = soc_indices_list


# Loop through the dictionary and filter each DataFrame based on IS_SOClist
filtered_dataframes = {}
for sheet_name, dataframe in dataframes_dict.items():
    filtered_dataframe = dataframe[dataframe.index.isin(IS_SOClist)]
    globals()[sheet_name] = filtered_dataframe  # Update the DataFrame in the global namespace
    filtered_dataframes[sheet_name] = filtered_dataframe


    # Find items in the IS_SOClist that are not in the DataFrame's index and print them
    not_in_df = [item for item in IS_SOClist if item not in dataframe.index]
    print(f"Sheet: {sheet_name}, Items not in DataFrame: {not_in_df}")


print(filtered_dataframes['Abilities_Importance'])



def calculate_job_pathways(abilities_importance_df, skills_importance_df, knowledge_importance_df,
                           abilities_level_df, skills_level_df, knowledge_level_df, IS_Salary_data_df):
    
    ability_mean = abilities_importance_df.mean().mean()
    skills_mean = skills_importance_df.mean().mean()
    knowledge_mean = knowledge_importance_df.mean().mean()
    print(ability_mean, skills_mean, knowledge_mean)
    
    ability_level_mean = abilities_level_df.mean().mean()
    skills_level_mean = skills_level_df.mean().mean()
    knowledge_level_mean = knowledge_level_df.mean().mean()
    print(ability_level_mean, skills_level_mean, knowledge_level_mean)
    
    ###
    ability_median = abilities_importance_df.mean().mean()
    skills_median = skills_importance_df.mean().mean()
    knowledge_median = knowledge_importance_df.mean().mean()
    print(ability_median, skills_median, knowledge_median)
    
    ability_level_median = abilities_level_df.mean().mean()
    skills_level_median = skills_level_df.mean().mean()
    knowledge_level_median = knowledge_level_df.mean().mean()
    print(ability_level_median, skills_level_median, knowledge_level_median)

    
    #HERE IS WHAT YOURE LOOKING FOR!! 
    
    ability_importance_cutoff = ability_mean
    skills_importance_cutoff = skills_mean
    knowledge_importance_cutoff = knowledge_mean
    ability_level_cutoff = ability_level_mean
    skills_level_cutoff = skills_level_mean
    knowledge_level_cutoff = knowledge_level_mean

    job_pathways_df = pd.DataFrame(index=abilities_importance_df.index, columns=abilities_importance_df.columns)
    pathway_summary_df = pd.DataFrame(index=abilities_importance_df.index,
                                      columns=['Yes', 'No: Salary', 'No: Skills Importance', 'No: Skills Level', 'No: Skills - Both', 'No: Level & Salary', 'No: Importance & Salary', 'No: All', ])

    # Initialize summary counts with zeros
    for row in abilities_importance_df.index:
        pathway_summary_df.loc[row, :] = 0

    for row in abilities_importance_df.index:
        
        median_skill = skills_importance_df.loc[row,:].median()
        median_ability = abilities_importance_df.loc[row,:].median()
        median_knowledge = knowledge_importance_df.loc[row, :].median()
        
        median_skill_l = skills_level_df.loc[row,:].median()
        median_ability_l = abilities_level_df.loc[row,:].median()
        median_knowledge_l = knowledge_level_df.loc[row, :].median()
        
        ability_importance_cutoff = median_ability
        skills_importance_cutoff = median_skill
        knowledge_importance_cutoff = median_knowledge
        ability_level_cutoff = median_ability_l
        skills_level_cutoff = median_skill_l
        knowledge_level_cutoff = median_knowledge_l
        
        for col in abilities_importance_df.columns:
            ability_importance = abilities_importance_df.loc[row, col]
            skills_importance = skills_importance_df.loc[row, col]
            knowledge_importance = knowledge_importance_df.loc[row, col]

            ability_level = abilities_level_df.loc[row, col]
            skills_level = skills_level_df.loc[row, col]
            knowledge_level = knowledge_level_df.loc[row, col]

            if ability_importance >= ability_importance_cutoff and skills_importance >= skills_importance_cutoff and knowledge_importance >= knowledge_importance_cutoff:
                
                if ability_level >= ability_level_cutoff and skills_level >= skills_level_cutoff and knowledge_level >= knowledge_level_cutoff:
                    
                    try:
                        old_job_median_earnings = IS_Salary_data_df.loc[row, 'Weighted Median Annual Earnings']
                        new_job_median_earnings = IS_Salary_data_df.loc[col, 'Weighted Pct. 75 Annual Earnings']
                    except KeyError:
                        job_pathways_df.loc[row, col] = 'error: salary data not found'
                        continue

                    if new_job_median_earnings >= old_job_median_earnings:
                        job_pathways_df.loc[row, col] = 'Y'
                        pathway_summary_df.loc[row, 'Yes'] += 1
                    else:
                        job_pathways_df.loc[row, col] = 'No: Salary'
                        pathway_summary_df.loc[row, 'No: Salary'] += 1
                else:
                    
                    try:
                        old_job_median_earnings = IS_Salary_data_df.loc[row, 'Weighted Median Annual Earnings']
                        new_job_median_earnings = IS_Salary_data_df.loc[col, 'Weighted Pct. 75 Annual Earnings']
                    except KeyError:
                        job_pathways_df.loc[row, col] = 'error: salary data not found'
                        continue
                    
                    if new_job_median_earnings >= old_job_median_earnings:
                        job_pathways_df.loc[row, col] = 'No: Skills Level'
                        pathway_summary_df.loc[row, 'No: Skills Level'] += 1
                    else:
                        job_pathways_df.loc[row, col] = 'No: Level & Salary'
                        pathway_summary_df.loc[row, 'No: Level & Salary'] += 1
                        
            else:
                
                if ability_level >= ability_level_cutoff and skills_level >= skills_level_cutoff and knowledge_level >= knowledge_level_cutoff:
                    
                    try:
                        old_job_median_earnings = IS_Salary_data_df.loc[row, 'Weighted Median Annual Earnings']
                        new_job_median_earnings = IS_Salary_data_df.loc[col, 'Weighted Pct. 75 Annual Earnings']
                    except KeyError:
                        job_pathways_df.loc[row, col] = 'error: salary data not found'
                        continue

                    if new_job_median_earnings >= old_job_median_earnings:
                        job_pathways_df.loc[row, col] = 'No: Skills Importance'
                        pathway_summary_df.loc[row, 'No: Skills Importance'] += 1
                    
                    else:
                        job_pathways_df.loc[row, col] = 'No: Importance & Salary'
                        pathway_summary_df.loc[row, 'No: Importance & Salary'] += 1
                         
                else:
                    
                    try:
                        old_job_median_earnings = IS_Salary_data_df.loc[row, 'Weighted Median Annual Earnings']
                        new_job_median_earnings = IS_Salary_data_df.loc[col, 'Weighted Pct. 75 Annual Earnings']
                    except KeyError:
                        job_pathways_df.loc[row, col] = 'error: salary data not found'
                        continue

                    if new_job_median_earnings >= old_job_median_earnings:
                        job_pathways_df.loc[row, col] = 'No: Skills - Both'
                        pathway_summary_df.loc[row, 'No: Skills - Both'] += 1
                    
                    else:
                        job_pathways_df.loc[row, col] = 'No: All'
                        pathway_summary_df.loc[row, 'No: All'] += 1

    # Sum across rows to get the total counts
    pathway_summary_df.loc['Total'] = pathway_summary_df.sum(axis=0)

    return job_pathways_df, pathway_summary_df



# Call the function and store the result in variables
job_pathways_matrix, summary_matrix = calculate_job_pathways(
    filtered_dataframes['Abilities_Importance'],
    filtered_dataframes['Skill_Importance'],
    filtered_dataframes['Knowledge_Importance'],
    filtered_dataframes['Abilities_Level'],
    filtered_dataframes['Knowledge_Level'],
    filtered_dataframes['Skill_Level'],
    Salary_data_df)
    
summary_matrix = summary_matrix.astype(float)

# Print the final matrix
print("Job Pathways Matrix:")
print(job_pathways_matrix)

# Print the summary matrix
print("\nSummary Matrix:")
print(summary_matrix)
print(type(summary_matrix.iloc[2, 2]))









'''
def calculate_job_pathways(abilities_similarity_df, skills_similarity_df, knowledge_similarity_df, IS_Salary_data_df):
    ability_mean = abilities_similarity_df.mean().mean()
    skills_mean = skills_similarity_df.mean().mean()
    knowledge_mean = knowledge_similarity_df.mean().mean()

    job_pathways_df = pd.DataFrame(index=abilities_similarity_df.index, columns=abilities_similarity_df.columns)
    pathway_summary_df = pd.DataFrame(index=abilities_similarity_df.columns, columns=['Ys', 'No: Salary', 'No: Skills', 'No: Both'])

    for col in abilities_similarity_df.columns:
        ys_count = 0.0
        no_salary_count = 0.0
        no_skills_count = 0.0
        no_both_count = 0.0

        for row in abilities_similarity_df.index:
            ability_similarity = abilities_similarity_df.loc[row, col]
            skills_similarity = skills_similarity_df.loc[row, col]
            knowledge_similarity = knowledge_similarity_df.loc[row, col]

            if ability_similarity > ability_mean and skills_similarity > skills_mean and knowledge_similarity > knowledge_mean:
                old_job_median_earnings = IS_Salary_data_df.loc[row, 'Weighted Median Annual Earnings']
                new_job_median_earnings = IS_Salary_data_df.loc[col, 'Weighted Median Annual Earnings']

                if new_job_median_earnings >= old_job_median_earnings:
                    job_pathways_df.loc[row, col] = 'Y'
                    ys_count += 1
                else:
                    job_pathways_df.loc[row, col] = 'No: Salary'
                    no_salary_count += 1
            else:
                if new_job_median_earnings >= old_job_median_earnings:
                    job_pathways_df.loc[row, col] = 'No: Skills'
                    no_skills_count += 1
                else:
                    job_pathways_df.loc[row, col] = 'No: Both'
                    no_both_count += 1


        pathway_summary_df.loc[col, 'Ys'] = ys_count
        pathway_summary_df.loc[col, 'No: Salary'] = no_salary_count
        pathway_summary_df.loc[col, 'No: Skills'] = no_skills_count
        pathway_summary_df.loc[col, 'No: Both'] = no_both_count
        


    return job_pathways_df, pathway_summary_df
'''