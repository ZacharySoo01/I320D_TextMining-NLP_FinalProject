import json
import csv
import sys

file_name = sys.argv[1]
# load json file and data
with open(file_name) as json_file:
    data = json.load(json_file)

# start csv writing
csv_file = open('arxiv_results.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)

# iterate through json data entries
first_iter = True
for entry in data:
    # extract headers on first iteration only
    if first_iter:
        csv_writer.writerow(entry.keys())
        first_iter = False

    # write values to csv rows
    title = entry['title'].replace('\n', ' ').strip('"').strip(' ')
    summary = entry['summary'].replace('\n', ' ').strip('"').strip(' ')
    csv_writer.writerow([title, summary])

csv_file.close()