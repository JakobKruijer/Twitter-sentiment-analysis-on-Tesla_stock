# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 15:00:22 2021

@author: jakob
"""
import pandas as pd
from scipy.stats import pearsonr
import plotly.io as pio
from bokeh.plotting import figure, show
import numpy as np
pio.renderers.default='browser'


#import data
df = pd.read_csv('Volume plus sentiment.csv')


#remove market closing days
df = df[:1006]

#descriptions of the data: mean, SD, range
# print(df["sentiment"].describe())
# print(df["Volume"].describe())
# print(df["Date"].describe())
# print(df["Close"].describe())

#correlation test (sentiment vs stock same day)
pearsonr(df["Volume"], df["sentiment"])

#Correlation graph
x=df["sentiment"]
y=df["Volume"]

# determine best fit line
par = np.polyfit(x, y, 1, full=True)
slope=par[0][0]
intercept=par[0][1]
y_predicted = [slope*i + intercept  for i in x]

# plot it
fig=figure(title="Correlation test",           
           x_axis_label="Sentiment score (-1 - 1)",
           y_axis_label="Difference in price (US Dollar)")
fig.circle(x,y, fill_alpha = 0.3)
fig.line(x,y_predicted,color='red',legend='y='+str(round(slope,2))+'x+'+str(round(intercept,2)))
show(fig)