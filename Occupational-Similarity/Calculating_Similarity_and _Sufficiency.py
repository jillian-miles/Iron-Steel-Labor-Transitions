#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 19:07:29 2023

@author: jillianmiles
"""

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Function to read data
def read_data(file_path):
    data = pd.read_excel(file_path)
    data = data[data['O*NET-SOC Code'].str.endswith('00')]
    data['O*NET-SOC Code'] = data['O*NET-SOC Code'].str[:-3]
    return data

# Function to format data for each category
def format_data(df, df_name):
    formatted_df = pd.DataFrame()

    for index, row in df.iterrows():
        o_net_soc_code = row['O*NET-SOC Code']
        element_name = row['Element Name']
        scale_name = row['Scale Name']
        data_value = row['Data Value']

        if scale_name == 'Level':
            if element_name not in formatted_df.columns:
                formatted_df[element_name] = pd.Series(dtype='float64')
            formatted_df.at[o_net_soc_code, element_name] = data_value
        elif scale_name == 'Importance':
            if element_name not in formatted_df.columns:
                formatted_df[element_name] = pd.Series(dtype='float64')
            formatted_df.at[o_net_soc_code, element_name] = data_value

    formatted_df.drop(columns=['O*NET-SOC Code'], inplace=True, errors='ignore')
    return formatted_df

# Function to calculate similarity based on Level
def calculate_level_similarity(df):
    similarity_matrix = pd.DataFrame(index=df.index, columns=df.index)
    num_skills = len(df.columns)

    for code1 in df.index:
        for code2 in df.index:
            if code1 == code2:
                similarity_matrix.loc[code1, code2] = 1
            else:
                sum_indicator = 0
                for skill in df.columns:
                    valx = df.loc[code1, skill]
                    valy = df.loc[code2, skill]
                    if valx >= valy:
                        indicator = 1 
                    else:
                        indicator = 0
                    sum_indicator += indicator
                similarity = sum_indicator / num_skills
                similarity_matrix.loc[code1, code2] = similarity
        print("done ", code1)
                
    return similarity_matrix


def calculate_level_similarity_bias_removed(df, df_importance):
    similarity_matrix = pd.DataFrame(index=df.index, columns=df.index)

    for code1 in df.index:
        for code2 in df.index:
            if code1 == code2:
                similarity_matrix.loc[code1, code2] = 1
            else:
                sum_indicator = 0
                num_skills = 0  # Initialize the count of relevant skills
                for skill in df.columns:
                    valx = df.loc[code1, skill]
                    valy = df.loc[code2, skill]
                    importance_valy = df_importance.loc[code2, skill]
                    
                    #RUNNING THE VALUE HERE
                    if importance_valy >= 3:
                        if valx >= valy:
                            indicator = 1 
                        else:
                            indicator = 0
                        sum_indicator += indicator
                        num_skills += 1  # Increment the count of relevant skills
                
                if num_skills > 0:
                    similarity = sum_indicator / num_skills
                    #print(code1, code2)
                    #print(sum_indicator)
                    #print(num_skills)
                    #print(similarity)
                else:
                    similarity = 0  # Avoid division by zero
                similarity_matrix.loc[code1, code2] = similarity
        print("done ", code1)
                
    return similarity_matrix



# Function to calculate similarity based on Importance
def calculate_importance_similarity(df):
    return pd.DataFrame(cosine_similarity(df.fillna(0)), columns=df.index, index=df.index)

# Read data
ONET_Abilities = read_data('/Users/jillianmiles/Documents/Academic/Research/data/ONET Downloads/Abilities.xlsx')
ONET_Skills = read_data('/Users/jillianmiles/Documents/Academic/Research/data/ONET Downloads/Skills.xlsx')
ONET_Knowledge = read_data('/Users/jillianmiles/Documents/Academic/Research/data/ONET Downloads/Knowledge.xlsx')

# Format data for each category
df_abilities_level = format_data(ONET_Abilities, 'Abilities')
df_abilities_importance = format_data(ONET_Abilities, 'Abilities')
df_skills_level = format_data(ONET_Skills, 'Skills')
df_skills_importance = format_data(ONET_Skills, 'Skills')
df_knowledge_level = format_data(ONET_Knowledge, 'Knowledge')
df_knowledge_importance = format_data(ONET_Knowledge, 'Knowledge')

# Function to count dimensions above or equal to 3 for each job code
def count_dimensions_per_job(importance_df, threshold=0):
    counts = importance_df.apply(lambda row: (row >= threshold).sum(), axis=1)
    return counts

# Calculate counts for  dimensions
abilities_counts = count_dimensions_per_job(df_abilities_importance)
skills_counts = count_dimensions_per_job(df_skills_importance)
knowledge_counts = count_dimensions_per_job(df_knowledge_importance)


# Calculate similarity matrices based on Level using the entire data
#abilities_level_similarity_matrix_all = calculate_level_similarity(df_abilities_level)
#skills_level_similarity_matrix_all = calculate_level_similarity(df_skills_level)
#knowledge_level_similarity_matrix_all = calculate_level_similarity(df_knowledge_level)

# Calculate similarity matrices based on Importance using the entire data
#abilities_importance_similarity_matrix_all = calculate_importance_similarity(df_abilities_importance)
#skills_importance_similarity_matrix_all = calculate_importance_similarity(df_skills_importance)
#knowledge_importance_similarity_matrix_all = calculate_importance_similarity(df_knowledge_importance)


#BIAS CONDITIONING

#Calculate similarity matrices based on Level using the entire data
#abilities_level_similarity_matrix_all_bias_removed = calculate_level_similarity_bias_removed(df_abilities_level, df_abilities_importance)
#skills_level_similarity_matrix_all_bias_removed = calculate_level_similarity_bias_removed(df_skills_level, df_skills_importance)
#knowledge_level_similarity_matrix_all_bias_removed = calculate_level_similarity_bias_removed(df_knowledge_level, df_knowledge_importance)


'''



### Print the resulting similarity matrices
print("Abilities Level Similarity Matrix:")
print(abilities_level_similarity_matrix)

print("Skills Level Similarity Matrix:")
print(skills_level_similarity_matrix)

print("Knowledge Level Similarity Matrix:")
print(knowledge_level_similarity_matrix)

print("Abilities Importance Similarity Matrix:")
print(abilities_importance_similarity_matrix)

print("Skills Importance Similarity Matrix:")
print(skills_importance_similarity_matrix)

print("Knowledge Importance Similarity Matrix:")
print(knowledge_importance_similarity_matrix)
'''