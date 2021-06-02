# Base packages
import os
import numpy as np
import pandas as pd
import re
import requests
from datetime import datetime

# Web scraping
from bs4 import BeautifulSoup

# Global vars
now = datetime.now()
timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")
data_path = "../data/newsData.xlsx"
expected_cols = ['Timestamp', 'Source', 'Headline']

def consolidate_data(new_data):
    """
    Function to save data automatically to form a historical base
    Args:
        new_data (pandas DataFrame): pandas DataFrame containing the latest headlines
    Returns:
        None
    """
    old_data = pd.read_excel(data_path)
    assert type(old_data) == pd.DataFrame
    assert list(old_data.columns) == expected_cols
    all_data = old_data.append(new_data)
    all_data.drop_duplicates(subset=['Headline'], inplace=True)
    all_data.to_excel(data_path, index=False)
    print(f"Data has been saved to {data_path}")

def collect_data(save_data=True, latest_only=False):
    """
    Function to return collected news headline from popular financial news sources
    Args:
        None
    Returns:
        news_df (pandas DataFrame): pandas DataFrame containing the news sources and their headlines
    """
    # FT response
    ft_response = requests.get("https://www.ft.com/")
    ft_soup = BeautifulSoup(ft_response.text, 'html.parser')
    ft_headlines_html = ft_soup.findAll("a", {"class": "js-teaser-heading-link"})
    ft_headlines = [item.getText() for item in ft_headlines_html]

    # Reuters response
    reuters_response = requests.get("https://www.reuters.com/")
    reuters_soup = BeautifulSoup(reuters_response.text, 'html.parser')
    reuters_headlines_html = reuters_soup.findAll("span", {"class": "MediaStoryCard__title___2PHMeX"})
    reuters_headlines = [item.getText() for item in reuters_headlines_html]

    # Bloomberg
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0',
        'From': 'marcus.aurelius@rome.com' 
    }

    bloomberg_response = requests.get("https://www.bloomberg.com/europe", headers=headers)
    bloomberg_soup = BeautifulSoup(bloomberg_response.text, 'html.parser')

    bloomberg_headlines_html_1 = bloomberg_soup.findAll("a", {"class": "single-story-module__headline-link"})
    bloomberg_headlines_html_2 = bloomberg_soup.findAll("a", {"class": "story-package-module__story__headline-link"})

    bloomberg_headlines_1 = [item.getText() for item in bloomberg_headlines_html_1]
    bloomberg_headlines_2 = [item.getText() for item in bloomberg_headlines_html_2]

    bloomberg_headlines = bloomberg_headlines_1 + bloomberg_headlines_2
    bloomberg_headlines = [re.sub(r"(\s\s+)|(\\n)", "", item) for item in bloomberg_headlines]

    # Unifying data sources
    news_df = pd.DataFrame(columns=["Timestamp", "Source", "Headline"])
    bloomberg_df = pd.DataFrame({"Timestamp": np.repeat(timestamp, len(bloomberg_headlines)),
                                 "Source": np.repeat("Bloomberg", len(bloomberg_headlines)),
                                 "Headline": bloomberg_headlines})
    ft_df = pd.DataFrame({"Timestamp": np.repeat(timestamp, len(ft_headlines)),
                          "Source": np.repeat("Financial Times", len(ft_headlines)),
                          "Headline": ft_headlines})
    reuters_df = pd.DataFrame({"Timestamp": np.repeat(timestamp, len(reuters_headlines)),
                                "Source": np.repeat("Reuters", len(reuters_headlines)),
                                "Headline": reuters_headlines})

    for df in [bloomberg_df, ft_df, reuters_df]:
        news_df = news_df.append(df)
        
    news_df.reset_index(drop=True, inplace=True)
    news_df.drop_duplicates(inplace=True)
    # Call the save_data function here!
    if save_data:
        consolidate_data(news_df)
    
    return news_df