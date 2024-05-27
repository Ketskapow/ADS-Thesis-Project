#%%
exec(open("preprocessing.py").read())

#%%
from datasets import DatasetDict

# Load the DatasetDict from the saved directory
loaded_dataset_dict = DatasetDict.load_from_disk(".")

# Now you have access to the loaded dataset dictionary
# You can access individual splits like loaded_dataset_dict['train'], loaded_dataset_dict['validation'], loaded_dataset_dict['test']
