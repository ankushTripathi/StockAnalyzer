import requests
import pandas as pd
import re
import flair
from datetime import datetime, timedelta


#pd.set_option('display.max_colwidth',None)

# re_whitespace = re.compile(r"\s+")
# re_web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
# re_user = re.compile(r"(?i)@[a-z0-9_]+")
# re_special = re.compile(r"[^a-zA-Z0-9]")
# re_stock = re.compile(r"(?i)@Tesla(?=\b)")

# passwdfile = open('TwitterAuthBearer.txt')
# try:
#     BEARER_TOKEN = passwdfile.readline()[:-1]
# finally:
#     passwdfile.close()

# endpoint = 'https://api.twitter.com/2/tweets/search/recent'
# headers = {'authorization': f'Bearer {BEARER_TOKEN}'}
# params = {
#     'query': '(tesla OR tsla OR elon musk) lang:en',
#     'max_results': '100',
#     'tweet.fields': 'created_at,lang'
# }

# dtformat = '%Y-%m-%dT%H:%M:%SZ'  # the date format string required by twitter

# # we use this function to subtract 60 mins from our datetime string
# def time_travel(now, mins):
#     now = datetime.strptime(now, dtformat)
#     back_in_time = now - timedelta(minutes=mins)
#     return back_in_time.strftime(dtformat)
    
# now = datetime.utcnow()  # get the current datetime, this is our starting point
# print(now)
# last_week = now - timedelta(days=6,hours=23)  # datetime one week ago = the finish line
# now = now.strftime(dtformat)  # convert now datetime to format for API

# df = pd.DataFrame()  # initialize dataframe to store tweets
# while True:
#     if datetime.strptime(now, dtformat) < last_week:
#         # if we have reached 7 days ago, break the loop
#         break
#     pre60 = time_travel(now, 60)  # get 60 minutes before 'now'
#     # assign from and to datetime parameters for the API
#     params['start_time'] = pre60
#     #params['end_time'] = now
#     response = requests.get(endpoint,
#                             params=params,
#                             headers=headers)  # send the request
#     if 'errors' in response.json():
#         raise Exception(response.json()['errors'])

#     now = pre60  # move the window 60 minutes earlier
#     # iteratively append our tweet data to our dataframe
#     for tweet in response.json()['data']:
        
#         clean_text = re_whitespace.sub(' ',tweet['text'])
#         clean_text = re_web_address.sub('', clean_text)
#         clean_text = re_stock.sub('tesla',clean_text)
#         clean_text = re_user.sub('',clean_text)
#         clean_text = re_special.sub(' ', clean_text)
#         clean_text = clean_text.lower()

#         tweet_datetime = datetime.strptime(tweet['created_at'],'%Y-%m-%dT%H:%M:%S.000Z')
#        # tweet_date = pd.to_datetime(tweet_datetime.date().strftime('%Y-%m-%d')).dt.date
#         tweet_date = tweet_datetime.date()
#         tweet_time = tweet_datetime.time().strftime('%H:%M:%S')

#         row = {'id' : tweet['id'], 'date' : tweet_date, 'time' : tweet_time, 'text' : clean_text}
#         df = df.append(row, ignore_index=True)

# sentiment_model = flair.models.TextClassifier.load('en-sentiment')    
# probs = []
# sentiments = []

# for tweet in df['text'].to_list():

#     sentence = flair.data.Sentence(tweet)
#     sentiment_model.predict(sentence)
#     probs.append(sentence.labels[0].score) 
#     sentiments.append(sentence.labels[0].value)

# df['probability'] = probs
# df['sentiment'] = sentiments

# df.to_csv('analyzed_tweets_tesla'+datetime.now().strftime('%Y-%m-%d_%H%M%S')+'.csv',sep='|',encoding='utf-8',index=False)
df = pd.read_csv('analyzed_tweets_tesla2021-04-15_115229.csv',sep='|',encoding='utf-8')

dataset = df[["id","date","sentiment","probability"]]
print(dataset['date'].unique().tolist())
dataset = dataset.groupby(["date","sentiment"])['probability'].mean()
print(dataset.head())
#dataset.to_csv('dataset'+datetime.now().strftime('%Y-%m-%d_%H%M%S')+'.csv',sep=',',encoding='utf-8',index=False)