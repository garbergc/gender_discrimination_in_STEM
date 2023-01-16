#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:44:03 2022

@author: eliserust
"""
## CREDIT: Sample framework code for this map was provided by Professor Hickman after working with him extensively
## Code was then generalized with for loops 

# Load necessary packages
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from plotly.offline import plot


# Load data
df = pd.read_csv("Clean_Datasets/OECD_LaborForce_Data.csv")

# Filter out year = 2005 to focus on annual measurements 2010 - 2019
df = df[df['Year'] != 2005] 

# Create list of dataframes by year
years = df.Year.unique().tolist()
years.sort()
dataframes = []

for year in years:
    df_year = df[df["Year"] == year]
    dataframes.append(df_year)

# Define all the columns that will be included in the dropdown menu
dropdown_columns = [
    "Agriculture, forestry, fisheries and veterinary",
    "Engineering, manufacturing and construction",
    "Health and welfare",
    "Information and Communication Technologies (ICTs)",
    "Natural sciences, mathematics and statistics",
    "Arts and humanities",
    "Business, administration and law",
    "Education",
    "Generic programmes and qualifications",
    "Services",
    "Social sciences, journalism and information",
]

# Initialize Graph Object
fig = go.Figure()
# Make base map white: https://plotly.com/python/map-configuration/
fig.update_geos(
    resolution=50,
    showland=True, landcolor="White"
)

# Define traces for all possible cases
# 11 fields x 11 years = 121 traces
# i.e. Trace  0 --> Agriculture in 2005

for dataframe in dataframes:
    for field in dropdown_columns:
        fig.add_trace(
            go.Choropleth(
                uid="set2",  # What is set2??
                locations=dataframe["COUNTRY"],  # Country Code
                z=dataframe[field],  # Data to be color-coded
                colorbar_title=field,
                coloraxis="coloraxis",
                visible=False,
                zmax=45,
                zmin=(-45),
                text=dataframe.apply(
                    lambda row: f"<b>Country: </b>{row['Country']}<br> <b>Difference: </b>{round(row[field], 3)}",
                    axis=1,
                ),
                hoverinfo="text",
            )
        )

# Make first trace visible

fig.data[0].visible = True


# DEFINE ONE SLIDE FOR EACH BUTTON
sliders = []
for item in dropdown_columns:
    steps = []
    for i, year in enumerate(years):
        step = dict(
            method="update",
            args=[
                {"visible": [False] * len(years)},
                # {"title": item + " in " + str(year)}
            ],  # layout attribute
            label=str(year),
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)
    slider1 = [
        dict(active=0, currentvalue={"prefix": "Year: "}, font = {"size":12}, pad={"t": 50}, steps=steps) # Add "Year" text to slider
    ]
    sliders.append(slider1)

# Initialize slider for Agriculture
fig.update_layout(sliders=sliders[0])


# ADD DROPDOWN TO CHANGE TYPE
# Define colorscale to match theme of dashboard
colorscale = ["#FF69B4", "#f49cc8", "#d9d2e9", "#8cbae0", "#4682B4"]

fig.update_layout(
    coloraxis_colorscale=colorscale,
    title="Difference in Share of Men and Women Entering Different Professional Fields <br><sup><i>Data Source: OECD Statistics 2018 (https://stats.oecd.org/Index.aspx?QueryId=109881)</i></sup>",
    title_x=0.1,
    # Create individual dictionaries for each dropdown menu item
    updatemenus=[
        dict(
            buttons=list(
                [
                    dict(
                        label="Agriculture, forestry, fisheries and veterinary",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                ]
                            },
                            {"sliders": sliders[0]},
                        ],
                    ),
                    dict(
                        label="Engineering, manufacturing and construction",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                ]
                            },
                            {"sliders": sliders[1]},
                        ],
                    ),
                    dict(
                        label="Health and welfare",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                ]
                            },
                            {"sliders": sliders[2]},
                        ],
                    ),
                    dict(
                        label="Information and Communication Technologies (ICTs)",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                ]
                            },
                            {"sliders": sliders[3]},
                        ],
                    ),
                    dict(
                        label="Natural sciences, mathematics and statistics",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                ]
                            },
                            {"sliders": sliders[4]},
                        ],
                    ),
                    dict(
                        label="Arts and humanities",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                ]
                            },
                            {"sliders": sliders[5]},
                        ],
                    ),
                    dict(
                        label="Business, administration and law",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                ]
                            },
                            {"sliders": sliders[6]},
                        ],
                    ),
                    dict(
                        label="Education",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    False,
                                    False,
                                    False,
                                ]
                            },
                            {"sliders": sliders[7]},
                        ],
                    ),
                    dict(
                        label="Generic programmes and qualifications",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    False,
                                    False,
                                ]
                            },
                            {"sliders": sliders[8]},
                        ],
                    ),
                    dict(
                        label="Services",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    False,
                                ]
                            },
                            {"sliders": sliders[9]},
                        ],
                    ),
                    dict(
                        label="Social sciences, journalism and information",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                ]
                            },
                            {"sliders": sliders[10]},
                        ],
                    ),
                ]
            ),
            direction="down",
            showactive=True,
            pad={"r": 10, "t": 10},
            x=0.9,
            xanchor="left",
            y=1.2,
            yanchor="top",
        ),
    ],
)


# Add legend title
fig.update_layout(
    coloraxis_colorbar=dict(
        title="<b>% Men Minus % Women Entering</b>",
        title_font_color = '#444444',
        title_font_size = 12
    ),
    hoverlabel = dict(
        font_size = 14),
    title_font = dict(size = 23)
)

fig.update_coloraxes(cmid=0)
fig.write_html("OECD_Novel_Viz.html", auto_open=True)
