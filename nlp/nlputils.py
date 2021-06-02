# Base packages
import os
import numpy as np
import pandas as pd
import re

# Config
import config

# Sentiment analysis
import torch
from transformers import AutoModelForSequenceClassification
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler

# General NLP libs
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
import string

# Tokenizer and sentiment classification models
tokenizer = config.TOKENIZER
model_path = config.BASE_MODEL_PATH
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Global vars
max_len = config.MAX_LEN
batch_size = config.BATCH_SIZE
label_dict = {0: 'positive', 1: 'negative', 2: 'neutral'}
stop_words = stopwords.words("english")
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x, axis=1)[:, None])
    return e_x / np.sum(e_x, axis=1)[:, None]

def extract_sentiment(news_df=None, 
                      print_results=False):
    input_ids = []
    attn_masks = []

    for (index, row) in news_df.iterrows():
        encoded_dict = tokenizer.encode_plus(row["Headline"],
                                            max_length=max_len,
                                            pad_to_max_length=True,
                                            truncation=True,
                                            return_tensors='pt')
        input_ids.append(encoded_dict['input_ids'])
        attn_masks.append(encoded_dict['attention_mask'])
        
    input_ids = torch.cat(input_ids, dim=0)
    attn_masks = torch.cat(attn_masks, dim=0)
    
    dataset = TensorDataset(input_ids, attn_masks)
    dataloader = DataLoader(dataset,
                            sampler = SequentialSampler(dataset),
                            batch_size = batch_size)
    
    # Running model
    print("Analyzing sentiments ...")
    model.eval()
    total_logits = []
    for batch in dataloader:
    # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask = batch
        with torch.no_grad():
            # Forward pass, calculate logit predictions
            outputs = model(b_input_ids, 
                            token_type_ids=None, 
                            attention_mask=b_input_mask)

        logits = outputs[0]
        total_logits.append(logits)
    
    flat_total_logits = np.concatenate(total_logits, axis=0)
    sentiment_indices = np.squeeze(np.argmax(softmax(flat_total_logits), axis=1))
    # Final results
    sentiment_list = [label_dict[item] for item in sentiment_indices]
    if print_results:
        print(pd.Series(sentiment_list).value_counts())
    return sentiment_list

def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<128)

def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub('[^a-zA-Z ]+', '', text)
    text = text.replace("nan", "")
    text = text.replace("None", "")
    text = removeNonAscii(text)
    text = re.sub(r'\b\w{0,2}\b', '', text) # Remove any words that are less than 3 characters longth
    text = text.strip()
    return text

def preprocess(column, stem=False, lemmatize=True):
    print("Tokenizing and cleaning text ...")
    column = [clean_text(row) for row in column]
    tokens = [word_tokenize(row) for row in column]
    preprocessed = []
    print("Carrying out core pre-processing processes ...")
    for val in tokens:
        row=[]
        for word in val:
            if word not in stop_words + list(string.punctuation):
                if stem == True:
                    row.append(ps.stem(word))
                elif lemmatize == True:
                    row.append(lemmatizer.lemmatize(word))
                else:
                    row.append(word)
        preprocessed.append(row)
    assert len(preprocessed) == len(column)
    return preprocessed

def get_wordcloud():
    pass

def model_topics():
    pass