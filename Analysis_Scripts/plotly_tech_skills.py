#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 22:39:26 2022

@author: claregarberg
"""

# final project: kaggle viz

# importing necessary libraries
import pandas as pd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot

# checking the working directory
path = os.getcwd()
path

kaggle = pd.read_csv("Clean_Datasets/Kaggle_WomenInDataScience_viz.csv")

# now let's take a look at the data
kaggle.head()
kaggle.columns

# dropping none and other
kaggle = kaggle[(kaggle.programming_skill != "None") & (kaggle.programming_skill != "Other")]

kaggle_m = kaggle[kaggle['gender'] == "Male"]
kaggle_m = kaggle_m.sort_values(by=['ratio'], ascending=True)

kaggle_f = kaggle[kaggle['gender'] == "Female"]
kaggle_f = kaggle_f.sort_values(by=['ratio'], ascending=True)

kaggle_m = kaggle_m.set_index("programming_skill")
kaggle_f = kaggle_f.set_index("programming_skill")

kaggle_m['ratio'] *= -1 # making male ratio negative

# creating bidirectional bar chart to show skills of mean and women

# plotly
# resource used: https://towardsai.net/p/l/tips-and-tricks-for-plotly-bar-chart, 
# resource used: https://community.plotly.com/t/subplots-how-to-add-master-axis-titles/13927/12
# resource used: https://stackoverflow.com/questions/68405808/dash-plotly-transform-into-an-absolute-value-for-hovertemplate
fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                    shared_yaxes=True, horizontal_spacing=0,
                    x_title='Percentage Of Respondents Of Each Gender Using On A Regular Basis',
                    y_title='Programming Tool',
                    subplot_titles=('Males',  'Females'))

fig.append_trace(go.Bar(y=kaggle_m.index, x=kaggle_m.ratio, orientation='h', width=0.4, 
                                 showlegend=False, marker_color='#4682B4', name="Males", meta=abs(kaggle_m.ratio),
                                 hovertemplate='%{meta:-.2%}'+'<br>Tool: %{y}'), 1, 1)

fig.append_trace(go.Bar(y=kaggle_f.index, x=kaggle_f.ratio, orientation='h', width=0.4, 
                                 showlegend=False, marker_color='#FF69B4', name="Females",
                                 hovertemplate='%{x:.2%}'+'<br>Tool: %{y}'), 1, 2)

fig.update_layout(title='Data Analytics Technical Skills By Gender',
                  title_font=dict(size=25, color='black', family="Open Sans"),
                  xaxis_range=[-0.33,0],
                  yaxis = dict(tickfont = dict(size=12)),
                  xaxis1 = dict(
                    tickmode = 'array',
                    tickvals = [-0.25, -0.2, -0.15, -0.1, -0.05],
                    ticktext = ['25%', '20%', '15%', '10%', '5%']),
                  xaxis2 = dict(
                    tickmode = 'array',
                    tickvals = [0, 0.05, 0.1, 0.15, 0.2, 0.25],
                    ticktext = ['0%', '5%', '10%', '15%', '20%', '25%']),
                  hoverlabel=dict(bgcolor="white", font_size=14, 
                                  font_family="Open Sans"))
fig.update_yaxes(ticklabelposition="inside")
fig.update_layout(plot_bgcolor = "white")
fig.update_xaxes(showline=True, linewidth=2, linecolor='grey', gridcolor='#C6C6C6')

plot(fig)

fig.write_html("kaggle_prog_skills.html")



