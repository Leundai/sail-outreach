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
import pandas as pd
sys.path.append('../')
from app import Schools, db

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

# TODO: Change path of file in order to be able to run in other machines.
def file_handler() -> None:
    school_row = 2
    count = 0
    print("Opening!")
    wb = xlrd.open_workbook(path_data)
    print("Its taking looong")
    sheet = wb.sheet_by_index(0)
    print("opened first sheet!")

    for school_row in range(sheet.nrows):
        row_data = sheet.row_values(school_row)

        # Skips all rows that are Districts not actual high schools
        if "District" == row_data[Type]:
            continue

        #Only to focus in any school that teaches seniors
        if "12" in str(row_data[Grades]):
            name = row_data[Name]
            city = row_data[City]
            num_of_students = int(row_data[Student_Count] or 0)
            white = float(row_data[White] or 0)
            black = float(row_data[Black] or 0)
            hispanic = float(row_data[Hispanic] or 0)
            asian = float(row_data[Asian] or 0)
            native = float(row_data[Native] or 0)
            pacific = float(row_data[Pacific] or 0)
            two_or_more = float(row_data[Two_or_More] or 0)
            low_income = float(row_data[Low_Income] or 0)

            
            school = Schools(
                name=name, city=city,
                num_of_students=num_of_students, percent_bl=black,
                percent_whit=white, percent_his=hispanic, percent_as=asian,
                percent_nat=native, percent_paci=pacific,
                percent_two=two_or_more, percent_low=low_income)
            db.session.add(school)
            
            print(school)
            count += 1
                
    db.session.commit()
    print("Number of Schools in database: %d" % (count))
    return None

def pandas_file_handler():
    csv_file = pd.read_csv(path_data, skiprows=6, skipfooter=7)
    print(csv_file)

#file_handler()
pandas_file_handler()
