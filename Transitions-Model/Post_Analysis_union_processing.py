#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 16:58:28 2024

@author: jillianmiles
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Path to your folder containing Excel files
folder_path = "/Users/jillianmiles/Documents/Academic/Research/Data/Union Results/"

# Initialize an empty list to store results
master_data = []

# Loop through all files in the folder
for file in os.listdir(folder_path):
    if file.endswith(".xlsx") or file.endswith(".xls"):  # Check for Excel files
        file_path = os.path.join(folder_path, file)
        
        # Extract the prefix and suffix from the filename
        try:
            base_name = os.path.splitext(file)[0]
            prefix, suffix = base_name.rsplit("_", 1)  # Split at the last underscore
            
            # Read the 2nd tab (usually index 1 in Python since it's zero-based)
            df = pd.read_excel(file_path, sheet_name="Supply Remaining")
            
            # Summation of the "Number of Workers" column
            total_workers = df["Number of Workers"].sum()
            
            # Append the data
            master_data.append({"Prefix": prefix, "Suffix": suffix, "Total Number of Workers": total_workers})
        except Exception as e:
            print(f"Error processing file {file}: {e}")

# Create a master DataFrame
master_df = pd.DataFrame(master_data)

# Reshape the DataFrame into the desired format
pivot_df = master_df.pivot(index="Prefix", columns="Suffix", values="Total Number of Workers")





# Remove unwanted rows
rows_to_remove = ["Base_AlleghenyPA", "Base_BAU Correct hopefully", "Base_San PatricioTX"]
pivot_df = pivot_df.drop(index=rows_to_remove, errors="ignore")


# Create a mapping dictionary
rename_mapping = {
    "Base_DuvalFl SCALED": "1xSEAF 1",
    "Base_FultonOH SCALED": "1xSEAF 2",
    "Base_JeffersonAL SCALED": "1xSEAF 3",
    "Base_JeffersonOH SCALED": "1xSEAF 4",
    "Base_MahoningOH SCALED": "1xSEAF 5",
    "Base_MeadeKY SCALED": "1xSEAF 6",
    "Base_DeKalbIN": "2xEAF 1",
    "Base_LowndesMS": "2xEAF 2",
    "Base_MontgomeryIN": "2xEAF 3",
    "Base_MorganAL": "2xEAF 4",
    "Base_WhitleyIN": "2xEAF 5"
}

# Rename the index of pivot_df using the mapping
pivot_df.rename(index=rename_mapping, inplace=True)

# Display the updated DataFrame
print(pivot_df)

pivot_df = pivot_df.reset_index()

# Sort Prefix in the desired order
pivot_df = pivot_df.sort_values(by='Prefix', key=lambda x: x.str.extract(r'(\d+)', expand=False).astype(int))




'''
# Plotting
pivot_df.plot(kind="bar", figsize=(10, 6), color=["#1f77b4", "#3399ff", "#66ccff"], edgecolor="black")

# Chart customization
plt.title("Grouped Bar Chart of Worker Totals by Scenario", fontsize=16)
plt.xlabel("Prefix", fontsize=14)
plt.ylabel("Total Number of Workers", fontsize=14)
plt.xticks(rotation=45, fontsize=12, ha="right")
plt.legend(title="Scenario", fontsize=12)
plt.tight_layout()

# Save the chart
plt.savefig("grouped_bar_chart.png")

# Display the chart
plt.show()

'''


# Plotting
ax = pivot_df.set_index("Prefix").plot(
    kind="bar", figsize=(20, 12),
    color=["#404040", "#8B0000", "#335577"],
    edgecolor="white"
)

# Customize axes
ax.set_title("Workers Not Transitioned by Scenario and Wage Premium Level", fontsize=16, fontweight='bold')
ax.set_xlabel("Scenario and Trial", fontsize=14, fontweight='bold')
ax.set_ylabel("Total Number of Workers Not Transitioned", fontsize=14, fontweight='bold')
ax.tick_params(axis='x', labelsize=12, rotation=45, labelcolor="black")
ax.tick_params(axis='y', labelsize=12, labelcolor="black")

# Legend - move outside the plot
ax.legend(
    title="Scenario", title_fontsize=12, fontsize=12, 
    loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0
)

# Grid and background
ax.set_facecolor("#F5F5F5")  # Light gray
plt.grid(visible=False)
plt.gca().set_axisbelow(True)

# Adjust layout for better appearance
plt.tight_layout(rect=[0, 0, 0.85, 1])  # Leave space on the right for the legend

# Display the plot
plt.show()






