library(dplyr)
library(caret)
library(ggplot2)
library(ggExtra)
library(gridExtra)
library(tidyr)
library(readr)
library(tidyverse)
library(data.table) 
library(plotly)

# load data
STEM_jobs <- read.csv(file = "Clean_Datasets/STEM_jobs.csv", header = T)

# correct column type
STEM_jobs$percent_of_men_earnings <- as.numeric(as.character(STEM_jobs$percent_of_men_earnings))
STEM_jobs$occupation_category <- as.factor(STEM_jobs$occupation_category)

# remove last row
STEM_jobs <- head(STEM_jobs, - 1) 

# remove NA rows
STEM_jobs <- STEM_jobs %>% drop_na()


# add lines
# vertical line at 100% (grey dotted line)
vline <- function(x = 0, color = "grey") {
  list(type = "line",
    y0 = 0,
    y1 = 1,
    yref = "paper",
    x0 = x,
    x1 = x,
    line = list(color = color, dash="dot"))
}

# horizontal line at 50% (grey dotted line)
hline <- function(y = 0, color = "grey") {
  list(type = "line",
    x0 = 0,
    x1 = 1,
    xref = "paper",
    y0 = y,
    y1 = y,
    line = list(color = color, dash="dot"))
}

# font details for main title
t_title <- list(family = "open sans",
  size = 25)

# font details for axis titles
t_axis <- list(family = "open sans",
  size = 18)

# plot
fig <- plot_ly(data=STEM_jobs, 
               y = ~percent_of_women, 
               x = ~percent_of_men_earnings, 
               color = ~occupation_category,
               colors = "Set1",
               size = ~total_employed,
               sizes = c(100,280), # adjust size range of points
               type = 'scatter',
               mode = 'markers',
               text = ~paste("Job: ", occupation)) # hover

fig <- fig %>% layout(title = list(text = "Women In STEM Occupations And Their Earnings",font = t_title), # main title
                      shapes = list(vline(100), hline(50)), # add lines
                      xaxis = list(ticksuffix = "%", 
                                   title = "Women's Earnings As A Percent Of Men's",
                                   zerolinecolor = 'gray60', 
                                   zerolinewidth = 2, 
                                   gridcolor = 'gray60',
                                   font = t_axis),
                      yaxis = list (ticksuffix = "%", 
                                    title = "Percent Of Women Employed",
                                    zerolinecolor = 'gray60', 
                                    zerolinewidth = 2, 
                                    gridcolor = 'gray60',
                                    font = t_axis),
                      legend=list(title=list(text='<b> Occupation Type </b>')),
                      annotations = 
                        # add data source on viz
                        list(x = -0.02, y = -0.10, # placement of text
                             text = "Source: https://www.census.gov/data/tables/time-series/demo/income-poverty/stem-occ-sex-med-earnings.html", 
                             showarrow = F, xref='paper', yref='paper', 
                             xanchor='left', yanchor='auto', xshift=0, yshift=0,
                             font=list(size=10, color="grey")),
                      margin = list(l = 60, r = 50, b = 100, t = 50, pad = 10))

# save figure
htmlwidgets::saveWidget(as_widget(fig), "STEM_jobs.html")







