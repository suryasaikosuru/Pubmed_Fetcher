import requests
import pandas as pd
import re
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

NON_ACADEMIC_KEYWORDS = ["Inc", "Ltd", "LLC", "Corporation", "Pharmaceuticals", "Biotech", "GmbH"]

def fetch_pubmed_ids(query: str) -> List[str]:
    """Fetch PubMed IDs matching the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 50  # Limit for testing
    }
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch details of papers by PubMed IDs."""
    if not pubmed_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    return parse_pubmed_xml(response.text)

def parse_pubmed_xml(xml_data: str) -> List[Dict]:
    """Parse PubMed XML data to extract required details."""
    root = ET.fromstring(xml_data)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pubmed_id = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text
        pub_date = article.find(".//PubDate/Year")
        pub_date = pub_date.text if pub_date is not None else "Unknown"

        authors = []
        non_academic_authors = []
        companies = []
        corresponding_email = None

        for author in article.findall(".//Author"):
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            affiliation = author.find("Affiliation")

            if last_name is not None and fore_name is not None:
                full_name = f"{fore_name.text} {last_name.text}"
                authors.append(full_name)

                if affiliation is not None:
                    aff_text = affiliation.text
                    if any(word in aff_text for word in NON_ACADEMIC_KEYWORDS):
                        non_academic_authors.append(full_name)
                        companies.append(aff_text)

            # Extract corresponding author email
            if author.find("Affiliation") is not None:
                emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", author.find("Affiliation").text)
                if emails:
                    corresponding_email = emails[0]

        papers.append({
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "; ".join(non_academic_authors),
            "Company Affiliation(s)": "; ".join(set(companies)),
            "Corresponding Author Email": corresponding_email or "N/A"
        })

    return papers

def save_to_csv(papers: List[Dict], filename: str) -> None:
    """Save papers to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
