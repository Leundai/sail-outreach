# -*- coding: utf-8 -*-

"""
Outreach File Processing
~~~~~~~~~~~~
This module takes in information from files for database storage
:by Leonardo Galindo 2020 
:license: Apache2, see LICENSE for more details.
"""

import sys
from pathlib import Path
from sqlalchemy.types import Integer, String
import pandas as pd
sys.path.append('../')

"""
TODO:
 - Expand this to other schools data
    - This can be done with automated click of button to check
        if the newest version is saved. (Or just automate)
    - This should be using
        https://nces.ed.gov/ccd/elsi/tableGenerator.aspx
"""

path_data = Path(__file__).parent / "../data/national.csv"

#This was created in reference to
#../data/illinois.xlsx
#Indices of the Spreadsheets
Type = 1
Name = 2
City = 4
Grades = 9
Student_Count = 15
White = 16
Black = 17
Hispanic = 18
Asian = 19
Native = 20
Pacific = 21
Two_or_More = 22
Low_Income = 26

def pandas_file_handler():
    #This is a recurring set of columns used to format and clean the dataframe
    demo_columns = [
        'percent_male', 'percent_fem', 'percent_two',
        'percent_paci', 'percent_whit', 'percent_bl',
        'percent_his', 'percent_as', 'percent_nat',
        'percent_low'
        ]

    dataframe = pd.read_csv(
        path_data,
        skiprows=6,
        skipfooter=7,
        engine='python',
        encoding='utf-8'
        )
    
    dataframe.columns = [
        'name', 'state',
        'st_abrv', 'county',
        'website', 'phone',
        'school_type', '12_offered',
        'num_of_students'] + demo_columns + ['city']

    dataframe["st_abrv"] = dataframe["st_abrv"].astype('str')
    dataframe["st_abrv"] = dataframe["st_abrv"].str.rstrip()

    #Cleanup of empty values/invalid
    dataframe = dataframe.replace(
        ['†', '–', '‡', '="0"'],
        ['0','0','0','0'],
        regex=True
        )

    #Changes all the values for students demographs into numeric
    dataframe[['num_of_students'] + demo_columns] = (dataframe[
        ['num_of_students'] + demo_columns]
        .apply(pd.to_numeric, errors='coerce')
        )

    #Divides each column row by its number of students and sets as percentage
    dataframe[demo_columns] = (dataframe[demo_columns]
        .div(dataframe['num_of_students'], axis=0)
        .round(3)
        .multiply(100)
        )
    dataframe = dataframe.fillna(0)

    return dataframe

def pandas_to_sql(dataframe, db):
    dataframe.to_sql(
        name='School',
        con=db.engine,
        index_label='id',
        if_exists='replace',
        dtype={
            'name': String(100),
            'state': String(100),
            'st_abrv': String(3),
            'county': String(100),
            'website': String(100),
            'phone': Integer,
            'school_type': String(100),
            '12_offered': String(100),
            'num_of_students': Integer,
            'percent_male': Integer,
            'percent_fem': Integer,
            'percent_two': Integer,
            'percent_paci': Integer,
            'percent_whit': Integer,
            'percent_bl': Integer,
            'percent_his': Integer,
            'percent_as': Integer,
            'percent_nat': Integer,
            'percent_low': Integer,
            'city': String(100)
        }
        )