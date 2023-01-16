## Data Munging
## OWID Female Labor Force & OECD Parental Leave

## libraries
library(tidyverse)
library(utils)

# checking working directory
getwd()

# reading in data
labor <- read.csv("Raw_Datasets/fertility-and-female-labor-force-participation.csv")
leave <- read.csv("Raw_Datasets/OECD_ParentalLeave.csv")

# first let's clean parental leave
summary(leave)

# dropping columns not needed (value is in weeks)
leave_clean <- subset(leave, select = c(Country, Indicator, Sex, Time, Value)) 
head(leave_clean) # we can see that the data is already aggregated 

write.csv(leave_clean, file="Clean_Datasets/parental_leave_CLEAN.csv")

# now let's clean labor participation
summary(labor)

# first let's rename the columns
names(labor) <- c("Country", "Code", "Year", "Female_labor_force_participation_rate", "Fertility_rate",
                  "Population", "Continent")

# dropping columns not needed
labor_clean <- subset(labor, select = -c(Code, Population, Continent)) 
head(labor_clean)

# dropping rows where we don't have labor force participation data
labor_clean <- labor_clean[complete.cases(labor_clean$Female_labor_force_participation_rate), ]
head(labor_clean)

# writing clean dataset to csv
write.csv(labor_clean, file="Clean_Datasets/female_labor_participation_CLEAN.csv")




