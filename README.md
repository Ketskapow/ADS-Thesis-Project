# ADS Thesis Project
 ADS thesis project of 2024 by Daniël Scheeper. Topic: "Using machine learning to study changes in ‘the nation’s mood’ in historical newspapers"

## Data overview
### 4-selected-data: 
Data after tf-idf was applied on 2-pre-selected-data. This data was used to predict the labels on.

The data is categorized depending on the certainty of the tf-idf prediction that the article deals with one of the chosen topics. We provide 4 levels of certainty: 99%, 98%, 95%, 90%. The higher the uncertainty the larger the number of articles contained in the selection, however the larger the probability that the article will not deal with the chosen topic.

### 5-labeled-sentiment:
Data chosen from 4-selected-data and labeled by labelers

- original_labeled: original files spitted out by the tool Label Studio used in this research

- Processed
    -	Uncleaned: same as Original_labeled
    -	Cleaned: cleaned text of labels (text processing)
    -	Merged: merged labels from two labelers using the procedure described below
    -	Merged_split: merged labels split on paragraphs of length of maximum 400 words.
## Labeling & merging
We selected two labelers to label the sentiment on each paragraph. This was done to improve the generalizability of the models and to avoid that the models would learn the subjective interpretation of one  labeler on the articles’ sentiments. Initially, the labels used ranged from -2 to +2 (-2 being very negative, +2 very positive). However, the labelers rarely used the extremes and this led us to downsize the range to three classes: -1;0;+1 (-1 being negative; +1 being positive). Finally, we gave the same set of paragraphs to be labeled to two labelers and then weighted their judgement in the following way.

-	If two labelers had diverging opinions (-1 and +1) or (+1 and -1), the example was discarded
-	If two labelers had similar opinions, we always preferred the most extreme one:
-	-1 and 0 -> -1
-	+1 and 0 -> +1
-	If two labelers had the same opinion, the label remained the same

# How to run
Preprocessing can be run by creating a data/ folder and placing the previously mentioned folders in this data folder. Model pipeline must be run in a colab environment. Word2vec and RobBERT pipelines require different environment setups, use requirements_word2vec.txt for the word2vec model, and the requirements.txt for the RobBERT model. Pretrained Word2Vec model was taken from https://github.com/clips/dutchembeddings, using the 160-dimensional combined embeddings.
