import sys
import threading
sys.path.append('../')
from app import Schools, db
import requests
import config

# Interval of 6 seconds per request
interval = 6
count_invervals = 0
MAX_INTERVALS = 3
NUM_OF_SCHOOLS = 1206

index = 1
def startTimer():
    threading.Timer(interval, startTimer).start()

    global index
    global count_invervals
    global MAX_INTERVALS

    if (count_invervals >= NUM_OF_SCHOOLS or count_invervals >= MAX_INTERVALS):
        print("Session Finished! Currently at index %d and interval %d" % (index, count_invervals))
        exit()
        return
    
    row = Schools.query.get(index)
    params = {"st": 'IL', "q": row.name, "city": row.city, "format": "json", "appID": config.appID, "appKey": config.apiKey}
    response = requests.get(f"https://api.schooldigger.com/v1.2/schools", params=params)
    count_invervals += 1

    if response.json()["numberOfSchools"] != 0:
        row.num_of_students = response.json()["schoolList"][0]["schoolYearlyDetails"][0]["numberOfStudents"]
        row.percent_af = response.json()["schoolList"][0]["schoolYearlyDetails"][0]["percentofAfricanAmericanStudents"]
        row.percent_as = response.json()["schoolList"][0]["schoolYearlyDetails"][0]["percentofAsianStudents"]
        row.percent_his = response.json()["schoolList"][0]["schoolYearlyDetails"][0]["percentofHispanicStudents"]
        row.percent_ind = response.json()["schoolList"][0]["schoolYearlyDetails"][0]["percentofIndianStudents"]
        row.percent_paci = response.json()["schoolList"][0]["schoolYearlyDetails"][0]["percentofPacificIslanderStudents"]
        row.percent_whit = response.json()["schoolList"][0]["schoolYearlyDetails"][0]["percentofWhiteStudents"]
        row.percent_two = response.json()["schoolList"][0]["schoolYearlyDetails"][0]["percentofTwoOrMoreRaceStudents"]
        row.percent_unsp = response.json()["schoolList"][0]["schoolYearlyDetails"][0]["percentofUnspecifiedRaceStudents"]
        row.percent_free = response.json()["schoolList"][0]["schoolYearlyDetails"][0]["percentFreeDiscLunch"]
        print(row)
        db.session.commit()
    else:
        print("Can't Find School!")
        print(row.name)

    index += 1

startTimer()