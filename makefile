scrape:
	rm arxiv_results.json
	rm arxiv_results.csv
	echo scraping arXiv ...
	python scrape.py
	echo converting json to csv ...
	python json_to_csv.py
	echo scraping process completed!