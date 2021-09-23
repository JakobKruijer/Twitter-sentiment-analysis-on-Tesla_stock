#How to https://betterprogramming.pub/how-to-scrape-tweets-with-snscrape-90124ed006af

# Imports
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data to
tweets_list = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('Tesla stock since:2017-01-01 until:2021-01-01').get_items()):
    tweets_list.append([tweet.date, tweet.content])

# Creating a dataframe from the tweets list above
tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'text'])

# save df in csv
tweets_df.to_csv('Tesla2017-20.csv', sep=',', index=False)
