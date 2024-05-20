from elasticsearch8 import Elasticsearch
from elasticsearch.helpers import bulk, BulkIndexError
from datetime import datetime
from dotenv import load_dotenv
import os
import json

# Load environment variables from elastic.env file
load_dotenv('elastic.env')

def main():
    # Read Elasticsearch credentials from environment variables
    es_username = os.getenv('ES_USERNAME')
    es_password = os.getenv('ES_PASSWORD')

    if not es_username or not es_password:
        print(f"ES_USERNAME: {es_username}")
        print(f"ES_PASSWORD: {es_password}")
        raise ValueError("Missing Elasticsearch credentials in environment variables")

    # Load local JSON data
    with open('twitter_word.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    filtered_rows = data["filtered_rows"]
    processed_data = []
    
    for row in filtered_rows:
        try:
            latitude = float(row["geo"]["latitude"])
            longitude = float(row["geo"]["longitude"])
        except (KeyError, ValueError, TypeError):
            # Skip this entry if latitude or longitude is missing or invalid
            continue

        processed_data.append(
            {
                "_index": "twitter-word",
                "_id": row["_id"],
                "_source": {
                    "created_at": datetime.strptime(row["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").isoformat() + 'Z',
                    "geo": {
                        "latitude": latitude,
                        "longitude": longitude,
                    },
                    "id": row["_id"],
                    "text": row["text"]
                }
            }
        )
    
    print(f"Processed {len(processed_data)} entries for bulk indexing.")

    # Elasticsearch client setup
    client = Elasticsearch(
        'https://127.0.0.1:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=(es_username, es_password),
        request_timeout=30  # Use request_timeout instead of timeout
    )

    # Initialize success and failed counts
    success = 0
    failed_docs = []

    # Bulk indexing with error handling
    try:
        success, _ = bulk(client, processed_data)
        print(f"Successfully indexed {success} documents.")
    except BulkIndexError as bulk_error:
        # Log details of the failed documents
        failed_docs = bulk_error.errors
        print(f"Failed to index {len(failed_docs)} documents.")
        for error in failed_docs:
            print(json.dumps(error, indent=2))

    return json.dumps({"status": "Completed", "success": success, "failed": len(failed_docs)})

if __name__ == "__main__":
    main()
