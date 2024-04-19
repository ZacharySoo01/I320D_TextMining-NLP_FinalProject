import urllib.request
import xml.etree.ElementTree as ET
import json

# Define the URL with the desired query parameters
base_url = 'http://export.arxiv.org/api/query?'
search_query = 'cat:cs.CL'  # Specify the taxonomy/category here, cs.AI for Artificial Intelligence
max_results = 1000  # Maximum number of results to retrieve

results = [] # list to store the results

def process(text: str) -> str:
    text = text.replace('\n', '')
    return ' '.join(list(filter(lambda x: x != '', text.split(' '))))

def request(url: str):
    # Open the URL and read the data
    with urllib.request.urlopen(url) as response:
        print(f'requesting page #{(start // 1000) + 1}')
        data = response.read().decode('utf-8')
        print(response.getcode())

    # Parse the XML response
    root = ET.fromstring(data)

    # Iterate through each entry in the XML response
    results = []
    num_results = 0
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        entry_dict = {}
        for elem in entry:
            if elem.tag.endswith('title'):
                num_results += 1
                entry_dict['id'] = start + num_results
                entry_dict['title'] = process(elem.text)
            elif elem.tag.endswith('summary'):
                entry_dict['summary'] = process(elem.text)

        results.append(entry_dict)
    print(f'{num_results} entries parsed')
    if num_results < 1000:
        print('trying again')
        return request(url)
    else:
        return results

global_results = []
for start in range(0, 10000, 1000):
    # Construct the full URL with query parameters
    url = f'{base_url}search_query={search_query}&start={start}&max_results={max_results}&sortBy=submittedDate'
    global_results += request(url)

# Output the results to a JSON file
output_file = 'arxiv_results.json'
with open(output_file, 'w') as json_file:
    json.dump(global_results, json_file, indent=4)

print(f"Results saved to {output_file}")
