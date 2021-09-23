import numpy as np
import pandas as pd
from os import path
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import re
from bs4 import BeautifulSoup


# maakt dataframe van tweets.csv en geeft columns mee
coll = ['date', 'text']
df = pd.DataFrame(pd.read_csv("TeslaTweets17-20.csv"), columns=coll)

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
df['text'] = df['text'].apply(tweet_cleaner)

# Maakt dataframe van text column
df = df.text
print(df)

#Haalt de woorden uit de tweets
tweets = df.values
words = str(tweets).split()

stopwords = set(STOPWORDS)
stopwords.update(["https", "cdnpoli", "co", "fd4CWiWVNK", "t"])


#telt de woorden en stopt de frequentie in de lijst
wordfreq = []
for i in words:
    wordfreq.append(words.count(i))

#maakt dataframe van woorden met bijbehorende frequentie
d = {'words': words, 'freq': wordfreq}
wordFreqDataframe = pd.DataFrame(d)
print(wordFreqDataframe)

# Create and generate a word cloud image:
wordcloud = WordCloud(stopwords = stopwords, max_font_size=75, max_words=100000, background_color="white").generate(df[1])
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# wordcloud.to_file("img/first_review.png")