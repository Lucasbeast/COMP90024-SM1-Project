from elasticsearch8 import Elasticsearch
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables from elastic.env file
load_dotenv('elastic.env')

def parse_datetime(date_str):
    """Parses datetime string with or without milliseconds"""
    for fmt in ('%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"no valid date format found for {date_str}")

def fetch_all_documents(client, index):
    """Fetches all documents from the specified index using the scroll API"""
    all_docs = []
    page = client.search(index=index, body={"query": {"match_all": {}}}, scroll='2m', size=1000)
    sid = page['_scroll_id']
    scroll_size = len(page['hits']['hits'])

    while scroll_size > 0:
        all_docs.extend(page['hits']['hits'])
        page = client.scroll(scroll_id=sid, scroll='2m')
        sid = page['_scroll_id']
        scroll_size = len(page['hits']['hits'])

    return all_docs

def main():
    # Read Elasticsearch credentials from environment variables
    es_username = os.getenv('ES_USERNAME')
    es_password = os.getenv('ES_PASSWORD')

    if not es_username or not es_password:
        print(f"ES_USERNAME: {es_username}")
        print(f"ES_PASSWORD: {es_password}")
        raise ValueError("Missing Elasticsearch credentials in environment variables")

    # Elasticsearch client setup
    client = Elasticsearch(
        'https://127.0.0.1:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=(es_username, es_password)
    )

    # Fetch all data from the 'twitter' index
    twitter_docs = fetch_all_documents(client, "twitter")
    twitter_dates = [hit["_source"]["created_at"] for hit in twitter_docs]
    
    twitter_dates = [parse_datetime(date) for date in twitter_dates]
    twitter_min_date = min(twitter_dates).strftime("%Y-%m-%d")
    twitter_max_date = max(twitter_dates).strftime("%Y-%m-%d")

    print(f"Twitter Data Time Span: {twitter_min_date} to {twitter_max_date}")

    # Fetch all data from the 'epa-alias' index
    epa_docs = fetch_all_documents(client, "epa-alias")
    epa_dates = []

    for hit in epa_docs:
        for param in hit["_source"]["parameters"]:
            start_date = param["startDateTime"]
            end_date = param["untilDateTime"]
            epa_dates.append((start_date, end_date))

    epa_start_dates = [parse_datetime(date[0]) for date in epa_dates]
    epa_end_dates = [parse_datetime(date[1]) for date in epa_dates]
    
    epa_min_start_date = min(epa_start_dates).strftime("%Y-%m-%d")
    epa_max_end_date = max(epa_end_dates).strftime("%Y-%m-%d")

    print(f"EPA Data Time Span: {epa_min_start_date} to {epa_max_end_date}")

if __name__ == "__main__":
    main()
