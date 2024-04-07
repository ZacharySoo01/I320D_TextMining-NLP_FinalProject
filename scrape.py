import urllib.request
import xml.etree.ElementTree as ET
import json

# Define the URL with the desired query parameters
base_url = 'http://export.arxiv.org/api/query?'
search_query = 'cat:cs.CL'  # Specify the taxonomy/category here, cs.AI for Artificial Intelligence
max_results = 1000  # Maximum number of results to retrieve

results = [] # list to store the results

for start in range(0, 11000, 1000):
    # Construct the full URL with query parameters
    url = f'{base_url}search_query={search_query}&start={start}&max_results={max_results}'

    # Open the URL and read the data
    with urllib.request.urlopen(url) as response:
        print(f'requesting page #{(start // 1000) + 1}')
        data = response.read().decode('utf-8')

    # Parse the XML response
    root = ET.fromstring(data)

    # Iterate through each entry in the XML response
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        entry_dict = {}
        for elem in entry:
            if elem.tag.endswith('title'):
                entry_dict['title'] = elem.text
            elif elem.tag.endswith('summary'):
                entry_dict['summary'] = elem.text
        results.append(entry_dict)

# Output the results to a JSON file
output_file = 'arxiv_results.json'
with open(output_file, 'w') as json_file:
    json.dump(results, json_file, indent=4)

print(f"Results saved to {output_file}")
