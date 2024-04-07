import json
import csv

# load json file and data
with open('arxiv_results.json') as json_file:
    data = json.load(json_file)

# start csv writing
csv_file = open('arxiv_results.csv', 'w')
csv_writer = csv.writer(csv_file)

# iterate through json data entries
first_iter = True
for entry in data:
    # extract headers on first iteration only
    if first_iter:
        csv_writer.writerow(data.keys())
        first_iter = False

    # write values to csv rows
    csv_writer.writerow(data.values())

csv_file.close()