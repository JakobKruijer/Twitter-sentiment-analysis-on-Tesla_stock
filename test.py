import pandas as pd
from textblob import TextBlob
from langdetect import detect
import re
from bs4 import BeautifulSoup

#Import TSLA stock data
df_stock = pd.read_csv('TeslaStock17-20.csv')

#Remove columns Open, High, Low, Adj Close, Volume
df_stock = df_stock.drop(columns=['Open', 'High', "Low", "Adj Close", "Volume"])

#Import Tesla Stock tweets between 2017 and 2021
df_tweets = pd.read_csv("TeslaTweets17-20.csv")

#cleaning text data https://towardsdatascience.com/another-twitter-sentiment-analysis-with-python-part-2-333514854913
from nltk.tokenize import WordPunctTokenizer
tok = WordPunctTokenizer()

pat1 = r'@[A-Za-z0-9_]+'
pat2 = r'https?://[^ ]+'
combined_pat = r'|'.join((pat1, pat2))
www_pat = r'www.[^ ]+'
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}
neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    try:
        bom_removed = souped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        bom_removed = souped
    stripped = re.sub(combined_pat, '', bom_removed)
    stripped = re.sub(www_pat, '', stripped)
    lower_case = stripped.lower()
    neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = [x for x  in tok.tokenize(letters_only) if len(x) > 1]
    return (" ".join(words)).strip()

#applying the text cleaning function to the text column
df_tweets['text'] = df_tweets['text'].apply(tweet_cleaner)

#Sentiment analysis
df_tweets['sentiment'] = df_tweets['text'].apply(lambda tweet: TextBlob(tweet).sentiment.polarity)

#Convert Datetime column type to datetime so that we can calculate the mean of each date (next step)
df_tweets["Datetime"] = pd.to_datetime(df_tweets["Datetime"])

#Calculate the mean of sentiment for each day 
df_tweets = df_tweets.resample('d', on='Datetime').mean().dropna(how='all')

#Reset the index so that the date becomes an column and not the index
df_tweets.reset_index(level=0, inplace=True)

#Convert the datetimecolumns in both dataframes to only show the date, and, rename Datetime column to 'Date' (in preparation of merge)
df_tweets["Datetime"] = pd.to_datetime(df_tweets["Datetime"]).dt.date
df_stock['Date'] = pd.to_datetime(df_stock['Date']).dt.date
df_tweets = df_tweets.rename(columns={'Datetime': 'Date'})

#Merge the df_tweets and df_stock dataframes based on the Date columns
merge = pd.merge(df_stock,df_tweets, how = 'outer', on = "Date")

#store in a csv
merge.to_csv('Price plus sentiment.csv', sep=',', index=False)

# ------------- Unused code --------------

# # #Detect language of each tweet 
# try:
#     df_tweets['Language'] = df_tweets['text'].apply(detect)
# except Exception:
#     pass
    
# # # #Filter for only english tweets
# df_tweets = df_tweets[df_tweets["Language"].str.contains("en")]

# # #Drop language column
# df_tweets = df_tweets.drop(columns= "Language")

# #Detect language of each tweet using TextBlob
# df_tweets['Language'] = df_tweets['text'].apply(lambda tweet: TextBlob(tweet).detect_language())

#Remove weekends from df_tweets
#df_tweets = df_tweets[df_tweets["Datetime"].dayofweek < 5]

#drop all na cells
#df_tweets["text"].dropna()