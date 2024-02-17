# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 19:10:48 2023

@author: micha
"""

import pandas as pd

# Load the data
anes_data = pd.read_csv("anes.csv", dtype={'VCF0703': str, 'VCF0301': str, 'VCF0104': str})

# Filter the data
relevant_vcf0703 = ['0', '1', '2']
filtered_data = anes_data[anes_data['VCF0703'].isin(relevant_vcf0703)]

# Group the data by VCF0104 and VCF0703
grouped_data = filtered_data.groupby(['VCF0104', 'VCF0703']).size().unstack(fill_value=0)
grouped_data['Total'] = grouped_data.sum(axis=1)

# Calculate percentages
for col in relevant_vcf0703:
    grouped_data[f'Percent_{col}'] = (grouped_data[col] / grouped_data['Total']) * 100

# Rename columns
grouped_data = grouped_data.rename(columns={
    'Percent_0': 'Pct_unregistered',
    'Percent_1': 'Pct_reg_novote',
    'Percent_2': 'Pct_voted'
})

# Create a new dataframe for VCF0104 data with the provided categories
vcf0104_data = pd.DataFrame({
    'VCF0104': ['1', '2', '3'],
    'Gender': ['Male', 'Female', 'Other']
})

# Merge with the grouped data
final_data = pd.merge(grouped_data.reset_index(), vcf0104_data, on='VCF0104')

# Group by the new VCF0104 categories (Gender) and calculate mean percentages
vcf0104_voter_data = final_data.groupby('Gender')[['Pct_unregistered', 'Pct_reg_novote', 'Pct_voted']].mean().reset_index()

# Sort the data if needed
sorted_voter_data = vcf0104_voter_data.sort_values(by='Gender', ascending=False)

# Print the sorted data
print(sorted_voter_data)
