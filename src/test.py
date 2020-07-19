import json

with open('data.txt') as json_file:
    data = json.load(json_file)
    print(data['index'])
    print(data['iteration'])