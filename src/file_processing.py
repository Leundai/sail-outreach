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
    CharterGrade = 11
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
    sheet = wb.sheet_by_index(School_Type.PublicSchool.value)

    for school_row in range(sheet.nrows):
        row_data = sheet.row_values(school_row)
        if "-12" in str(row_data[Col_Index.GradeServed.value]):
            name = row_data[Col_Index.Name.value]
            city = row_data[Col_Index.CityPublicPrivate.value]
            type_of = sheet.name
            school = Schools(name=name, city=city, type_of=type_of)
            db.session.add(school)
            print(school)
    db.session.commit()

file_handler()
Schools.query.all()