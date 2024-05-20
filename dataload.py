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
            dataframes_per_year[year] = df
        else:
            # If dataframe for the year already exists, merge them
            dataframes_per_year[year] = pd.concat([dataframes_per_year[year], df])

# Combine all dataframes into a single dataframe
combined_df = pd.concat(dataframes_per_year.values(), ignore_index=True)
