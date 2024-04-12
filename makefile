scrape:
	rm arxiv_results.json
	rm arxiv_results.csv
	echo scraping arXiv ...
	python scrape.py
	echo converting json to csv ...
	python json_to_csv.py arxiv_results.json
	echo scraping process completed!