PubMed Research Paper Fetcher:
OVERVIEW:
This Python program fetches research papers from PubMed based on a user-specified query. It identifies papers with at least one author affiliated with a pharmaceutical or biotech company and outputs the results in a CSV file
Installation 
Prerequisites :
Ensure you have Python 3.8+ installed on your system. 
Install Poetry :
curl -sSL https://install.python-poetry.org python3 
Clone the Repository :
git clone <your-github-repo-url> 
cd pubmed_fetcher 
Install Dependencies 
poetry install 
Usage 
Command-Line Arguments 
query (required): Search query for PubMed. 
---debug: Enable debug mode. 
--file <filename>: Specify the output CSV filename. 
Run the Program 
poetry run get-papers-list "COVID-19 vaccine" -f results.csv 
To print results to the console: 
poetry run get-papers-list "COVID-19 vaccine" 
Enable debug mode: 
poetry run get-papers-list "COVID-19 vaccine" 
Code Structure 
pubmed_fetcher/
-
pubmed_fetcher/
_init__.py 
fetch_papers.py 
cli.py 
i Fetches and filters PubMed papers 
pyproject.tomi 
