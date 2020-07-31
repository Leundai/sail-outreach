#Ignore this file, it is entirely useless

import sys
import json
import threading
sys.path.append('../')
from app import Schools, db
import requests
import config

# Interval of 6 seconds per request
interval = 6
count_invervals = 0
MAX_INTERVALS = 500 #We can't make more than 500 calls otherwise we get bogus data
NUM_OF_SCHOOLS = 1206 # All schools in database that may or may not have data
index = 0

with open('index.txt', 'r+') as json_file:
    data = json.load(json_file)
    count_invervals = data['iteration']
    index = data['index']

# TODO: Populate the missing schools with data that school digger api doesn't contain
def startQuery():
    threading.Timer(interval, startQuery).start()

    global index
    global count_invervals
    global MAX_INTERVALS

    # TODO: This doesn't finish the actual program, it keeps stating Session Finished.
    if (count_invervals >= NUM_OF_SCHOOLS or count_invervals >= MAX_INTERVALS):
        with open('index.txt', 'w+') as json_file:
            data = {}
            data['iteration'] = 0
            data['index'] = index
            json.dump(data, json_file)

        print("Session Finished! Currently at index %d and interval %d" % (index, count_invervals))
        exit()
        return
    
    # Ask Leo for API Key or make your own through school digger, currently using the Basic Plan
    row = Schools.query.get(index)
    params = {"st": 'IL', "q": row.name, "city": row.city, "format": "json", "appID": config.appID, "appKey": config.apiKey}
    response = requests.get(f"https://api.schooldigger.com/v1.2/schools", params=params)
    count_invervals += 1
    index += 1

    with open('index.txt', 'w+') as json_file:
        data = {}
        data['iteration'] = count_invervals
        data['index'] = index
        json.dump(data, json_file)

    print(count_invervals)

    # TODO: Find a way of making this prettier?
    # Goes through the json response and only selects the first index it returns if there even is a school
    if response.json()["numberOfSchools"] != 0: # Fix: School Digger returns nothing when you are at max calls
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

startQuery()