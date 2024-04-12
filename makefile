scrape:
	rm arxiv_results.json
	rm arxiv_results.csv
	python scrape.py
	python json_to_csv.py arxiv_results
	

scrape-test:
	rm test_data.json
	rm test_data.csv
	python scrape_small.py
	python json_to_csv.py test_data
	