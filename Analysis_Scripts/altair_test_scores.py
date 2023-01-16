#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 7 17:21:35 2022
@author: kajaltiwary
"""

## Install all necessary libraries
## Python code formatted via black tool
import pandas as pd
from pandas import DataFrame
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import altair as alt

## Read in clean test scores data
testscores = pd.read_csv("Clean_Datasets/OECD_Test_Scores_Clean.csv")

## Remove the last two columns of the data frame
testscores = testscores.iloc[:, :-2]

## Remove countries with one/few data point(s)
testscores = testscores[
    testscores["country_code"].str.contains("PER|COL|MAC|TWN|HKG|SGP|CRI|LTU|IDN")
    == False
]

## Calculate the average test score for all countries
test = (
    testscores.groupby(["gender", "subject", "year"])["test_score"].mean().reset_index()
)

## Combine the new data frame with the original test scores data frame
testscores = pd.concat([test, testscores])

## Add a country column for the average values
testscores[["country_code"]] = testscores[["country_code"]].fillna("ALL")

## Rename columns for aesthetics on the chart
testscores.rename(
    columns={
        "subject": "Subject",
        "year": "Year",
        "gender": "Gender",
        "test_score": "Test_Score",
        "country_code": "Country_Code",
    },
    inplace=True,
)

## Convert year column to correct date format for visualization
testscores["Year"] = pd.to_datetime(testscores["Year"], format="%Y")

## Rename subject values for chart aesthetics
conditions = [
    (testscores["Subject"] == "read"),
    (testscores["Subject"] == "math"),
    (testscores["Subject"] == "science"),
]
choices = ["Reading", "Math", "Science"]
testscores["Subject"] = np.select(conditions, choices)

## Rename gender values
conditions = [
    (testscores["Gender"] == "boy"),
    (testscores["Gender"] == "girl"),
    (testscores["Gender"] == "tot"),
]
choices = ["Boy", "Girl", "Total"]
testscores["Gender"] = np.select(conditions, choices)

## Round values to two decimal points for aesthetics
testscores["Test_Score"] = testscores["Test_Score"].round(decimals=2)

## Sort country code values alphabetically for drop down
testscores = testscores.sort_values("Country_Code")

## Create dropdown values and filters
## Website used: https://altair-viz.github.io/user_guide/interactions.html
drop_down = alt.binding_select(
    name=" Country: ", options=list(testscores["Country_Code"].unique())
)
drop_down_filter = alt.selection_single(
    fields=["Country_Code"],
    bind=drop_down,
    name=" Country: ",
    init={"Country_Code": "ALL"},
)

## Develop line chart with tool tip and drop down
## Website used: https://stackoverflow.com/questions/60838082/altair-line-chart-with-stroked-point-markers
## Website used: https://github.com/altair-viz/altair/issues/1947
## Website used: https://altair-viz.github.io/user_guide/customization.html
## Website used: https://altair-viz.github.io/gallery/multi_series_line.html
figure = (
    alt.Chart(
        testscores,
        title="Average PISA Test Scores By Subject And Gender From 2000-2018 (Every Three Years)",
    )
    .mark_line(point={"filled": False, "fill": "white"})
    .encode(
        x=alt.X("Year", axis=alt.Axis(title="Year")),
        y=alt.Y(
            "Test_Score", axis=alt.Axis(title="Test Score"), scale=alt.Scale(zero=False)
        ),
        row=alt.Row(
            "Subject:O",
            spacing=16,
            title=None,
            header=alt.Header(
                labels=True,
                labelFontWeight="bold",
                labelAngle=0,
                labelOrient="top",
                labelFont="Open Sans",
                labelFontSize=13,
                labelBaseline="top",
            ),
            center=True,
        ),
        color=alt.Color(
            "Gender",
            legend=alt.Legend(
                title="Gender",
                titleFontSize=12,
                titleFont="Open Sans",
                labelFont="Open Sans",
                labelFontSize=12,
            ),
            scale=alt.Scale(range=["#4682B4", "#FF69B4", "#4DAF4A"]),
        ),
        tooltip=[
            alt.Tooltip("Year:T", format="%Y"),
            "Subject",
            "Gender",
            "Test_Score",
            "Country_Code",
        ],
    )
    .properties(width=780, height=200)
    .resolve_axis(y="independent")
    .interactive()
    .add_selection(drop_down_filter)
    .transform_filter(drop_down_filter)
)


## Define annotation that contains source used and data set used
## Website used: https://altair-viz.github.io/user_guide/generated/core/altair.TitleParams.html
figure = alt.concat(
    figure,
    title=alt.TitleParams(
        "Source: OECD (https://data.oecd.org/pisa/reading-performance-pisa.htm#indicator-chart) | Data File: OECD_Test_Scores_Clean.csv",
        color="black",
        baseline="bottom",
        orient="bottom",
        anchor="start",
        fontSize=10,
        font="Open Sans",
        dy=10,
    ),
)

## Change the font and size of the axes to match overall theme
## Website used: https://stackoverflow.com/questions/54855337/increase-font-size-of-chart-title-in-altair
figure = figure.configure_axis(
    labelFontSize=12, titleFontSize=12, labelFont="Open Sans", titleFont="Open Sans"
)

## Change the font and size of the title to match overll theme
## Website used: https://altair-viz.github.io/gallery/ridgeline_plot.html?highlight=configure_title
figure = figure.configure_title(
    offset=5, orient="top", anchor="middle", fontSize=22, font="Open Sans"
)

## Save grouped-line and faceted plot to html file
figure.save("test_scores_altair.html")
