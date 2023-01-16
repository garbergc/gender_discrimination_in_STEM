#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 21:19:56 2022
@author: kajaltiwary
"""

## Install all necessary libraries
## Python code formatted via black tool
import pandas as pd
from pandas import DataFrame
import numpy as np
import xarray as xr
import plotly.express as px
import plotly.graph_objects as go
import os
import altair as alt

## Read in appropriate data and store in variable
combined_df = pd.read_csv("Clean_Datasets/female_labor_participation_CLEAN.csv")

## Filter dataframe to only keep the OECD countries
combined_df = combined_df[
    combined_df["Country"].str.contains(
        "Australia|Austria|Belgium|Canada|Chile|Colombia|Costa Rica|Czech Republic|Denmark|Estonia|Finland|France|Germany|Greece|Hungary|Iceland|Ireland|Isreal|Italy|Japan|Korea|Latvia|Lithuania|Luxembourg|Mexico|Netherlands|New Zealand|Norway|Poland|Portugal|Slovak Republic|Slovenia|Spain|Sweden|Switzerland|Turkey|United Kingdom|United States"
    )
    == True
]

## Rename country values for chart aesthetics
combined_df["Country"] = combined_df["Country"].replace(
    {"United States Virgin Islands": "Virgin Islands"}
)

## Remove all duplicate values
combined_df.drop_duplicates(keep=False)

## Define the encoding to link the views together
## Website used: https://altair-viz.github.io/user_guide/compound_charts.html
link_parameter = alt.selection(type="single", encodings=["y"])

## Convert time to appropriate date format
combined_df["Year"] = pd.to_datetime(combined_df["Year"], format="%Y")

## Define the color scheme of valeus
## Green gradient to denote neutral scheme
color_scheme = ["#4DAF4A", "#013220"]

## First, create a bar chart with the average labor force participation rate over time by country
## Make sure encoding is applied so that this chart is the anchor for link transformations
## Website used: https://altair-viz.github.io/gallery/bar_chart_horizontal.html
## Website used: https://altair-viz.github.io/user_guide/interactions.html
bar_chart = (
    alt.Chart(
        combined_df, title="Average Female Labor Force Participation From 1960-2020"
    )
    .mark_bar()
    .encode(
        x=alt.X(
            "mean(Female_labor_force_participation_rate):Q",
            axis=alt.Axis(title="Average Female Labor Force Participation Rate (%)"),
        ),
        y=alt.Y("Country:N", axis=alt.Axis(title="Country"), sort="-x"),
        color=alt.condition(
            link_parameter, alt.ColorValue("#4DAF4A"), alt.ColorValue("grey")
        ),
        tooltip=[
            alt.Tooltip(
                "mean(Female_labor_force_participation_rate):Q",
                title="Avg Labor Force Participation",
                format=".2f",
            ),
            "Country",
        ],
    )
    .add_selection(link_parameter)
    .interactive()
    .properties(width=300, height=760)
)

## Second, define a scatter plot with fertility and labor force participation rate
## Make sure the transform filter is applied to link view to the bar chart
## Website used: https://altair-viz.github.io/gallery/bubble_plot.html
## Website used: https://www.geeksforgeeks.org/how-to-color-a-scatter-plot-by-a-variable-in-altair/
scatter_chart = (
    alt.Chart(
        combined_df,
        title="Female Labor Force Participation And Fertility Rate From 1960-2020",
    )
    .mark_point()
    .encode(
        x=alt.X(
            "Female_labor_force_participation_rate",
            axis=alt.Axis(title="Female Labor Force Participation Rate (%)"),
        ),
        y=alt.Y("Fertility_rate", axis=alt.Axis(title="Fertility Rate (%)")),
        size=alt.Size("Year"),
        color=alt.Color(
            "Year",
            scale=alt.Scale(range=color_scheme),
            legend=alt.Legend(
                format="%Y",
                titleFontSize=12,
                titleFont="Open Sans",
                labelFont="Open Sans",
                labelFontSize=12,
            ),
        ),
        tooltip=[
            alt.Tooltip("Year:T", format="%Y"),
            alt.Tooltip("Fertility_rate", title="Fertility Rate", format=".2f"),
            alt.Tooltip(
                "Female_labor_force_participation_rate",
                title="Labor Force Participation",
                format=".2f",
            ),
            "Country",
        ],
    )
    .transform_filter(link_parameter)
    .interactive()
    .properties(width=850, height=300)
)

## Third, define a boxplot to see the distribution of fertility rate by country
## Make sure the transform filter is applied to link view to the bar chart
## Website used: https://altair-viz.github.io/gallery/boxplot.html
## Website used: https://stackoverflow.com/questions/71022972/manually-calculate-the-boxplot-whiskers-in-altair
box_chart = (
    alt.Chart(
        combined_df, title="Fertility Rate Distribution By Country From 1960-2020"
    )
    .mark_boxplot(size=20)
    .encode(
        x=alt.X("Country:N", axis=alt.Axis(title="Country")),
        y=alt.Y(
            "Fertility_rate:Q", scale=alt.Scale(zero=False), title="Fertility Rate (%)"
        ),
        color=alt.Color("Country", legend=None, scale=alt.Scale(range=["#4DAF4A"])),
    )
    .transform_filter(link_parameter)
    .interactive()
    .properties(width=850, height=300)
)


## Concatenate the box and scatter plots vertically
## Website used: https://stackoverflow.com/questions/60328943/how-to-display-two-different-legends-in-hconcat-chart-using-altair
total = alt.vconcat(box_chart, scatter_chart,).resolve_legend(
    color="independent", size="independent"
)

## Concatenate the bar chart to the combined box and scatter plot display
## Website used: https://stackoverflow.com/questions/60328943/how-to-display-two-different-legends-in-hconcat-chart-using-altair
total = alt.hconcat(bar_chart, total,).resolve_legend(
    color="independent", size="independent"
)

## Define the annotation to add to the bottom of the dashboard
## Website used: https://altair-viz.github.io/user_guide/generated/core/altair.TitleParams.html
total = alt.concat(
    total,
    title=alt.TitleParams(
        "Source: OWID (https://ourworldindata.org/grapher/fertility-and-female-labor-force-participation) | Data File: female_labor_participation_CLEAN.csv",
        color="black",
        baseline="bottom",
        orient="bottom",
        font="Open Sans",
        fontSize=10,
        dy=20,
    ),
)

## Website used: https://stackoverflow.com/questions/54855337/increase-font-size-of-chart-title-in-altair
total = total.configure_axis(
    labelFontSize=12, titleFontSize=12, labelFont="Open Sans", titleFont="Open Sans"
)

## Website used: https://altair-viz.github.io/gallery/ridgeline_plot.html?highlight=configure_title
total = total.configure_title(fontSize=20, font="Open Sans")

## Save combined altair dashboard to html file
total.save("fertility_part_dashboard.html")
