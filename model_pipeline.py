#%%
from datasets import DatasetDict

# Load the DatasetDict from the saved directory
data = DatasetDict.load_from_disk(".")

#%%
from transformers import AutoModel, AutoTokenizer
import torch

model_ckpt = "distilbert-base-uncased"

#%%
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)

#function that tokenizes, we use padding and truncation in order to have consistent input dimensions for the model. This improves model training.
def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True)

#%%
#map the function to all three datasets in the dict
data_encoded = data.map(tokenize, batched=True, batch_size=None)