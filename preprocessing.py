# %%
import pandas as pd
import os

# Define the directory path where the files are located
directory = 'data/5-labeled-sentiment/dataMaud/'

# Initialize an empty dictionary to store dataframes for each year
df_per_year = {}

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Extract year and fuel type from the filename
        year, fuel_type = filename.split('_')[0], filename.split('_')[1].split('.')[0]

        # Load the CSV file into a dataframe
        df = pd.read_csv(os.path.join(directory, filename))

        # Add a new column for fuel type
        df['fuel_type'] = fuel_type
        df['year'] = year

        # Add the dataframe to the dictionary using year as key
        if year not in df_per_year:
            df_per_year[year] = df
        else:
            # If dataframe for the year already exists, merge them
            df_per_year[year] = pd.concat([df_per_year[year], df])

# %%
# Function to check if 'labeler3' values exist in 'labels_edo' or 'labels_marin'
def check_labels(data_dict):
    results = {}
    for key, df in data_dict.items():
        # Check if 'labeler3' values are in 'labels_edo' or 'labels_marin'
        try:
            exists_in_either = df['labeler3'].isin(df['labels_edo']).any() or df['labeler3'].isin(df['labels_marin']).any()
            results[key] = exists_in_either
        except:
            print('an exception occurred')

    return results

results_dict = check_labels(df_per_year)

for key, val in results_dict.items():
    print(key, val)


# %%
df_per_year['1970s'].rename(columns={'labele3': 'labeler3'})
df_per_year['1960s'] = df_per_year['1960s'][['text', 'labels', 'fuel_type', 'year']]
# create merged dataset for labeler3
for key, df in df_per_year.items():
    try:
        df_per_year[key] = df[['text_split', 'labeler3', 'fuel_type', 'year']].rename(columns={'text_split':'text', 'labeler3':'labels'})
    except:
        print('an exception occurred')
#%%
directory = 'data/5-labeled-sentiment/labeled-full/processed/merged'

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Extract year and fuel type from the filename
        year, fuel_type, _ = filename.split('_')
        # Load the CSV file into a dataframe
        df = pd.read_csv(os.path.join(directory, filename), usecols=['text', 'labels'])
        # Add a new column for fuel type
        df['fuel_type'] = fuel_type
        df['year'] = year

        # Add the dataframe to the dictionary using year as key
        if year not in df_per_year:
            df_per_year[year] = df
        else:
            # If dataframe for the year already exists, merge them
            df_per_year[year] = pd.merge(df_per_year[year], df, on=['text', 'fuel_type', 'labels', 'year'], how='outer')

# Now, df_per_year contains the merged dataframes without duplicates


# %%
concatenated_df = pd.concat(df_per_year, ignore_index=True)

#%%
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict

# Split your data into train, validation, and test sets using scikit-learn
X_train_val, X_test, y_train_val, y_test = train_test_split(concatenated_df['text'], concatenated_df['labels'], test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.2, random_state=42)

# Convert your splits into dictionaries
train_data = {
    'text': X_train,
    'label': y_train
}

val_data = {
    'text': X_val,
    'label': y_val
}

test_data = {
    'text': X_test,
    'label': y_test
}

# Convert each split into a Dataset
train_dataset = Dataset.from_dict(train_data)
val_dataset = Dataset.from_dict(val_data)
test_dataset = Dataset.from_dict(test_data)

# Store the datasets in a DatasetDict
dataset_dict = DatasetDict({
    'train': train_dataset,
    'validation': val_dataset,
    'test': test_dataset
})


#%%
import os
import pickle

# Create the directory if it doesn't exist
directory = './data/preprocessed/'
if not os.path.exists(directory):
    os.makedirs(directory)

# Export df_per_year to a file
with open(os.path.join(directory, 'df_per_year.pkl'), 'wb') as f:
    pickle.dump(df_per_year, f)

dataset_dict.save_to_disk(".")
