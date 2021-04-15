import requests
from stockanalyzer import TwitterSearchUrl
from stockanalyzer import TwitterAuthBearer 
from stockanalyzer import TickerNames
import pandas as pd
import re

import flair

pd.set_option('display.max_colwidth',None)

re_whitespace = re.compile(r"\s+")
re_web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
re_user = re.compile(r"(?i)@[a-z0-9_]+")
re_special = re.compile(r"[^a-zA-Z0-9]")
    

def cleanText(re_stock,stock_name,tweet):
    clean_text = re_whitespace.sub(' ',tweet)
    clean_text = re_web_address.sub('', clean_text)
    clean_text = re_stock.sub(stock_name,clean_text)
    clean_text = re_user.sub('',clean_text)
    #clean_text = re_special.sub(' ', clean_text)
    clean_text = clean_text.lower()
    return clean_text

def get(ticker):
    stock_name = TickerNames[ticker]
    re_stock = re.compile(r"(?i)@"+stock_name+"(?=\b)")
    params = { 'q' : stock_name, 'tweet_mode' : 'extended', 'lang' : 'en', 'count' : '100'}
    headers = {'authorization' : 'Bearer '+TwitterAuthBearer}
    response  = requests.get(TwitterSearchUrl,params=params,headers=headers)
    tweets = response.json()
    
    df = pd.DataFrame()
    for tweet in tweets['statuses']:
        row = {'id' : tweet['id_str'], 'created_at' : tweet['created_at'], 'text' : cleanText(re_stock,stock_name,tweet['full_text'])}
        df = df.append(row,ignore_index=True)

    return df

def analyse(df):
    
    sentiment_model = flair.models.TextClassifier.load('en-sentiment')    
    probs = []
    sentiments = []

    for tweet in df['text'].to_list():

        sentence = flair.data.Sentence(tweet)
        sentiment_model.predict(sentence)
        probs.append(sentence.labels[0].score) 
        sentiments.append(sentence.labels[0].value)
    
    df['probability'] = probs
    df['sentiment'] = sentiments

    return df