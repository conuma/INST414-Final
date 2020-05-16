# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 16:33:58 2020

@author: cathe
"""

import pandas as pd
import numpy as np
from collections import Counter
import re

west = ['WA', 'OR', 'CA', 'MT', 'ID', 'WY', 'NV', 'UT', 'CO', 'NM', 'AZ', 'AK', 'HI']
northeast = ['PA', 'NJ', 'NY', 'CT', 'RI', 'MA', 'VT', 'NH', 'ME'] 
midwest = ['ND', 'SD', 'NE', 'KS', 'MO', 'IA', 'MN', 'IL', 'WI', 'IN', 'OH', 'MI']
south = ['TX', 'OK', 'AR', 'LA', 'MS', 'AL', 'GA', 'FL', 'TN', 'SC', 'NC', 'KY', 'VA', 'WV', 'DC', 'MD', 'DE']

glassdoor = pd.read_csv("C:/Users/cathe/glassdoor4.csv", header=0)

print(glassdoor.dtypes)
def form(i):
    result = float(i)
    return result
glassdoor['rating'] = glassdoor['rating'].map(form)

# check for missing values
print(glassdoor.isnull().sum())

# drop unnamed column and location column
glassdoor_df = glassdoor.drop(['Unnamed: 0', 'headquarters'], axis=1)

print(glassdoor_df)

# check for duplicate rows
duprows_df = glassdoor_df[glassdoor_df.duplicated()]
print("duplicated rows:")
print(duprows_df)
percent_dup = (len(duprows_df)/len(glassdoor_df))*100
print(str(round(percent_dup, 2))+"% of the dataframe are duplicates")

# drop duplicates
glassdoor_df = glassdoor_df.drop_duplicates()
print("dropped duplicates")
print(glassdoor_df)

# delete rows with missing values
glassdoor_df = glassdoor_df[glassdoor_df.interview_difficulty != '-']
glass = glassdoor_df.dropna()
print("dropped missing values")
print(glass)

# reformat location column

def mode(i):
    if '[' in i:
        split_it = i.split(',')
        counter = Counter(split_it) 
        most_occur = counter.most_common(1)
        most = ' '.join([str(elem) for elem in most_occur]).split(',')
        most1 = most[0].split("'")
        return most1[1]
    else:
        return i

glass['location'] = glass['location'].map(mode)
print(glass['location'])

def level(i):
    match = re.match('[A-Z]{2}', i)
    if match:
        if match.group() in west:
            return "West"
        if match.group() in south:
            return "South"
        if match.group() in northeast:
            return "Northeast"
        if match.group() in midwest:
            return "Midwest"
    else:
        return "other"

glass['location'] = glass['location'].map(level)
print(glass['location'])

replace_map = {'location': {'Midwest': 1, 'Northeast': 2, 'South': 3, 'West': 4, 'other': 5}}
labels = glass['location'].astype('category').cat.categories.tolist()
replace_map_comp = {'location' : {k: v for k,v in zip(labels,list(range(1,len(labels)+1)))}}

print(replace_map_comp)
glass.replace(replace_map_comp, inplace=True)

print(glass.head())

# reformat company size
glass['company_size'].unique()
def size(i):
    if '10000+' in i or '1001 to 5000' in i or '5001 to 10000' in i:
        return "Big"
    if '201 to 500' in i or '501 to 1000' in i:
        return "Medium"
    if 'Unknown' in i or '51 to 200' in i or '1 to 50' in i:
        return "small"

glass['company_size'] = glass['company_size'].map(size)
print(glass['company_size'])

#replace_map1 = {'company_size': {'Big': 1, 'Medium': 2, 'small': 3}}
labels1 = glass['company_size'].astype('category').cat.categories.tolist()
replace_map_comp1 = {'company_size' : {k: v for k,v in zip(labels1,list(range(1,len(labels1)+1)))}}

print(replace_map_comp1)
glass.replace(replace_map_comp1, inplace=True)

print(glass.head())
print(glass['company_size'])

# reformat revenue
glass['revenue'].unique()
def rev(i):
    if '+' in i:
        splt = i.split('+')
        return splt[0]+"000000000"
    if 'to' in i and 'billion' in i:
        splt = i.split('to ')[1].split(' billion')
        return splt[0]+"000000000"
    if 'to' in i and 'million' in i:
        splt = i.split('to ')[1].split(' million')
        return splt[0]+"000000"
    if 'Less' in i:
        return ' $1000000'
    if 'Unknown' in i:
        return ' $1000000'
    
glass['revenue'] = glass['revenue'].map(rev)
print(glass['revenue'])

def num(i):
    splt = i.split('$')
    return splt[1]
glass['revenue'] = glass['revenue'].map(num)
print(glass['revenue'])   
glass['revenue'] = glass['revenue'].astype(np.int64)

def std(i):
    stndize = i/1000000000
    return stndize
glass['revenue'] = glass['revenue'].map(std)
print(glass['revenue'])   

print(glass.dtypes)
# check for outliers
print("Checking for outlier in rating column:")
q1 = glass['rating'].quantile(0.25)
q3 = glass['rating'].quantile(0.75)
IQR = q3-q1

lowerRange = (q1-1.5)*IQR
upperRange = (q3+1.5)*IQR

print(lowerRange)
print(upperRange)
print(glass.boxplot(column=['rating']))
print(glass['rating'].describe())

print(" ")
print("Checking for outliers in revenue column: ")
q1_rev = glass['revenue'].quantile(0.25)
q3_rev = glass['revenue'].quantile(0.75)
IQR_rev = q3_rev-q1_rev

lowerRange_rev = (q1_rev-1.5)*IQR_rev
upperRange_rev = (q3_rev+1.5)*IQR_rev

print(lowerRange_rev)
print(upperRange_rev)
print(glass.boxplot(column=['revenue']))
print(glass['revenue'].describe())

print(" ")
print("Checking for outliers in interview_difficulty column: ")
glass['interview_difficulty'] = glass['interview_difficulty'].astype(float)
q1_diff = glass['interview_difficulty'].quantile(0.25)
q3_diff = glass['interview_difficulty'].quantile(0.75)
IQR_diff = q3_diff-q1_diff

lowerRange_diff = (q1_diff-1.5)*IQR_diff
upperRange_diff = (q3_diff+1.5)*IQR_diff

print(lowerRange_diff)
print(upperRange_diff)
print(glass.boxplot(column=['interview_difficulty']))

print(glass['interview_difficulty'].describe())

# Summary of categorical variables
glass['location'].value_counts()
glass['company_size'].value_counts()
glass['glassdoor_awards'].value_counts()
glass['other_awards'].value_counts()


# save cleaned dataframe as csv file
glass.to_csv("glassdoor_clean.csv")
print("saved to glassdoor_clean.csv")
print(glass.info)
print(glass.dtypes)
