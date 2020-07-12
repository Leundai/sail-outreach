import xlrd
from enum import Enum
import sys
sys.path.append('../')
from app import Schools, db

#This was created in reference to excel sheet 
#https://www.isbe.net/_layouts/15/Download.aspx?SourceUrl=/Documents/dir_ed_entities.xls
class Col_Index(Enum):
    RecType = 1
    Name = 5
    GradeServed = 12
    CharterSpecEdGrade = 11
    CitySpecEdCharter = 8
    CityPublicPrivate = 9

class School_Type(Enum):
    PublicSchool = 1
    SpecEd = 2
    PrivateSchool = 5
    CharterSchool = 7

def file_handler(input_file=r"D:\\Documents\\repos\\sail-outreach\\dir_ed_entities.xls"):
    school_row = 2
    wb = xlrd.open_workbook(input_file)

    for school_type in School_Type:
        sheet = wb.sheet_by_index(school_type.value)
        city_index = Col_Index.CityPublicPrivate.value
        grade_index = Col_Index.GradeServed.value

        if (school_type == School_Type.SpecEd or school_type == School_Type.CharterSchool):
            city_index = Col_Index.CitySpecEdCharter.value
            grade_index = Col_Index.CharterSpecEdGrade.value
            

        for school_row in range(sheet.nrows):
            row_data = sheet.row_values(school_row)

            if school_type == School_Type.PublicSchool and "Dist" in row_data[Col_Index.RecType.value]:
                continue

            #Only to focus in any school that teaches seniors
            if "-12" in str(row_data[grade_index]):
                name = row_data[Col_Index.Name.value]
                city = row_data[city_index]
                type_of = sheet.name
                school = Schools(name=name, city=city, type_of=type_of)
                db.session.add(school)
                print(school)
                
    db.session.commit()

file_handler()