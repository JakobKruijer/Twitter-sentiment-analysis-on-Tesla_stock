# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 12:24:43 2021

@author: jakob
"""
import pandas as pd
from scipy.stats import pearsonr
import plotly.io as pio
from bokeh.plotting import figure, show
import numpy as np
pio.renderers.default='browser'

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

#import data
df = pd.read_csv('Price plus sentiment.csv')

#calculate the difference in price each day
df['Close_dif'] = df['Close'].diff()

#remove market closing days
df = df[418:450]

# #descriptions of the data: mean, SD, range
# print(df["sentiment"].describe())
# print(df["Close_dif"].describe())
# print(df["Date"].describe())
# print(df["Close"].describe())

# #correlation test (sentiment vs stock same day)
# pearsonr(df["Close_dif"], df["sentiment"])

# #Correlation graph
# x=df["sentiment"]
# y=df["Close_dif"]

# # determine best fit line
# par = np.polyfit(x, y, 1, full=True)
# slope=par[0][0]
# intercept=par[0][1]
# y_predicted = [slope*i + intercept  for i in x]

# # plot it
# fig=figure(title="Correlation test",           
#            x_axis_label="Sentiment score (-1 - 1)",
#            y_axis_label="Difference in price (US Dollar)")
# fig.circle(x,y, fill_alpha = 0.3)
# fig.line(x,y_predicted,color='red',legend='y='+str(round(slope,2))+'x+'+str(round(intercept,2)))
# show(fig)

# df["Date"] = pd.to_datetime(df["Date"])

#create bar plot for average temps by month
plt.title('Average Temperature by Month')
sns.barplot(x='Date', y='sentiment', data=df, palette='summer')

# create line plot for average percipitation levels
plt.title('Twitter sentiment on Tesla stock and Tesla stock market price')
sns.lineplot(x='Date', y='Close', data=df, sort=False)

#Create combo chart
fig, ax1 = plt.subplots(figsize=(15,6))
color = 'tab:green'
#bar plot creation
ax1.set_title('Twitter sentiment on Tesla stock and Tesla stock market price', fontsize=16)
ax1.set_xlabel('Month', fontsize=16)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=40, ha="right")
ax1.set_ylabel('Sentiment', fontsize=16, color=color)
ax1 = sns.barplot(x='Date', y='sentiment', data = df, palette='summer')
ax1.tick_params(axis='y')
#specify we want to share the same x-axis
ax2 = ax1.twinx()
color = 'tab:red'
#line plot creation
ax2.set_ylabel('Stock price (US Dollars)', fontsize=16, color=color)
ax2 = sns.lineplot(x='Date', y='Close', data = df, sort=False, color=color)
ax2.tick_params(axis='y', color=color)



#show plot
plt.show()

# ---------- unused code -------------
#correlation test (sentiment vs stock next day)
# df['sentiment_shift'] = df['sentiment'].shift(1)
# df = df[1:]
# pearsonr(df["Close_dif"], df["sentiment_shift"])

