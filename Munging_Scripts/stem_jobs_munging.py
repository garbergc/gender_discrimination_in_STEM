import pandas as pd
import numpy as np
import xlrd
import openpyxl

# load data
STEM_jobs_original = pd.read_excel('Raw_Datasets/Table1_STEM _STEM-Related_Occupations (1).xlsx', index_col=None, header=None)

# remove rows 0-7 and bottom 16
STEM_jobs = STEM_jobs_original.drop(STEM_jobs_original.index[0:10])
STEM_jobs = STEM_jobs.drop(STEM_jobs.index[130:])
STEM_jobs = STEM_jobs.reset_index()
STEM_jobs = STEM_jobs[[0, 1, 3, 5, 7, 9, 11, 13, 15]]

# change column names
STEM_jobs.columns = ['occupation',
                    'total_employed', 'men_employed', 'women_employed', 'percent_of_women',
                    'total_median_earnings', 'men_earnings', 'women_earnings', 'percent_of_men_earnings']

# remove "..." from occupation column
STEM_jobs['occupation'] = STEM_jobs.occupation.str.strip('...')

# create new column for occupation categories that contains the occupation rows with ":"
STEM_jobs["occupation_category"] = STEM_jobs['occupation'].str.contains(':')

# empty list
occupation_category = [0]*len(STEM_jobs['occupation'])

# fill the list with the occupation category for each occupation
for i in range(len(STEM_jobs['occupation_category'])):
    if STEM_jobs['occupation_category'][i] == True:
        occupation_category[i] = STEM_jobs['occupation'][i]
        j = STEM_jobs['occupation'][i]
    else:
        occupation_category[i] = j

# fill occupation_category column with the occupation_category list
STEM_jobs["occupation_category"] = occupation_category

# shift column 'occupation_category' to second position
second_column = STEM_jobs.pop('occupation_category')
STEM_jobs.insert(1, 'occupation_category', second_column)

# remove ":"
STEM_jobs = STEM_jobs[STEM_jobs["occupation"].str.contains(":") == False]
STEM_jobs['occupation_category'] = STEM_jobs.occupation_category.str.strip(':')

# export CSV file
STEM_jobs.to_csv('STEM_jobs.csv', index = False, header=True)




