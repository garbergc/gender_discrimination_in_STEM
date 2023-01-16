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
library(curl)

# load data
df <- read.csv(file = "Clean_Datasets/parental_leave_CLEAN.csv", header = T)

# remove first column and Sex columns (not needed)
df <- subset(df, select = -X)
df <- subset(df, select = -Sex)

# correct column type
df$Country <- as.factor(df$Country)
df$Year <- as.factor(df$Time)
df$Indicator <- as.factor(df$Indicator)

# remove rows with condition
# df <- df[!grepl("Length of parental leave with job protection", df$Indicator),]
df <- df[!grepl("Total length of paid maternity and parental leave", df$Indicator),]

# order countries
df <- df %>% group_by(Country, Year, Indicator) %>% arrange(-Value)
df$Country <- factor(df$Country, levels = unique(df$Country)[order(df$Value, decreasing = TRUE)])

# change wording in Indicator column
df$Indicator <- gsub('Length of maternity leave', 'Maternity Leave', df$Indicator)
df$Indicator <- gsub('Length of paid father-specific leave', 'Paternity Leave (Paid)', df$Indicator)
df$Indicator <- gsub('Length of parental leave with job protection', 'Total Parental Leave <br>With Job Protection', df$Indicator)

# remove countries that have missing data
#summary(df$Country) # used this to find with contries had less than 63 values
# list of countries that have missing values
remove <- c('Estonia', 'Latvia', 'Lithuania',
            'OECD - Average', 'Slovenia',
            'Chile', 'Israel', 'Costa Rica')
# remove rows that contain any string in the vector in the Country column
df <- df[!grepl(paste(remove, collapse='|'), df$Country),]

# font details for main title
t_title <- list(family = "open sans",
  size = 25)

# font details for axis titles
t_axis <- list(family = "open sans",
  size = 18)

# plot
fig <- plot_ly(df, 
               x = ~Value, 
               y = ~reorder(Country, -Value), 
               color = ~Indicator, 
               colors = c("#FF69B4", "#4682B4", "#4DAF4A"), # pink, blue, green
               frame = ~Year, # cycle through year in animation 
               type = "bar")
fig <- fig %>% layout(title = list(text = "Government Granted Parental Leave By Country",font = t_title), # main title
                      xaxis = list(  
                        zerolinecolor = 'gray60',  
                        zerolinewidth = 2,  
                        gridcolor = 'gray60', # grey grid lines
                        title = "Weeks",
                        font = t_axis),  
                      yaxis = list(  
                        zerolinecolor = 'gray60',  
                        zerolinewidth = 2,  
                        gridcolor = 'gray60', # grey grid lines
                        title = "Country",
                        categoryarray = ~Country, # sets order of countries listed on the y axis 
                        type = "category", # countries are categorical
                        categoryorder = "total ascending", # refresh sort the country names 
                        font = t_axis),
                      legend = list(title=list(text='<b> Parental Leave Type </b>')),
                      annotations = 
                        # add data source on viz
                        list(x = 0, y = -0.1, # placement of text
                             text = "Source: https://stats.oecd.org/index.aspx?queryid=54760", 
                             showarrow = F, xref='paper', yref='paper', 
                             xanchor='left', yanchor='auto', xshift=0, yshift=0,
                             font=list(size=10, color="grey")),
                      margin = list(l = 60, r = 50, b = 150, t = 50, pad = 10))

# timing and animation
fig <- fig %>%
  animation_opts(1000, # timing
    easing = "elastic", # animation
    redraw = TRUE) # reorder the countries 


# save figure
htmlwidgets::saveWidget(as_widget(fig), "parental_Leave.html")
