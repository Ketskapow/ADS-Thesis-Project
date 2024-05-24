# %%
import pandas as pd
import os

# Define the directory path where the files are located
directory = 'data/5-labeled-sentiment/dataMaud/'

# Initialize an empty dictionary to store dataframes for each year
dataframes_per_year = {}

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Extract year and fuel type from the filename
        year, fuel_type = filename.split('_')[0], filename.split('_')[1].split('.')[0]

        # Load the CSV file into a dataframe
        df = pd.read_csv(os.path.join(directory, filename))

        # Add a new column for fuel type
        df['Fuel_Type'] = fuel_type

        # Add the dataframe to the dictionary using year as key
        if year not in dataframes_per_year:
            dataframes_per_year['maud', year] = df
        else:
            # If dataframe for the year already exists, merge them
            dataframes_per_year[year] = pd.concat([dataframes_per_year[year], df])

# %%
merged_dfs_per_year = {}
data1960maud = dataframes_per_year.pop(('maud', '1960s'))
merged_dfs_per_year[('maud', '1960s')] = data1960maud

# %%
# Function to check if 'labeler3' values exist in 'labels_edo' or 'labels_marin'
def check_labels(data_dict):
    results = {}
    for key, df in data_dict.items():
        # Check if 'labeler3' values are in 'labels_edo' or 'labels_marin'
        exists_in_either = df['labeler3'].isin(df['labels_edo']).any() or df['labeler3'].isin(df['labels_marin']).any()
        results[key] = exists_in_either

    return results

results_dict = check_labels(dataframes_per_year)

for key, val in results_dict.items():
    print(key, val)



#%%
directory = 'data/5-labeled-sentiment/labeled-full/processed/cleaned'

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        person, year, fuel_type = filename.split('_')

        df = pd.read_csv(os.path.join(directory, filename))

        df['Fuel_Type'] = fuel_type

        if year not in dataframes_per_year:

