from elasticsearch8 import Elasticsearch
from elasticsearch.exceptions import RequestError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('elastic.env')

def create_twitter_index():
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

    # Define the index settings and mapping
    index_body = {
        "settings": {
            "index": {
                "number_of_shards": 3,
                "number_of_replicas": 1
            }
        },
        "mappings": {
            "properties": {
                "created_at": {
                    "type": "date"
                },
                "geo": {
                    "properties": {
                        "latitude": {
                            "type": "float"
                        },
                        "longitude": {
                            "type": "float"
                        }
                    }
                },
                "id": {
                    "type": "keyword"
                },
                "sentiment": {
                    "type": "float"
                }
            }
        }
    }

    # Create the index
    try:
        client.indices.create(index='twitter-testpw', body=index_body)
        print("Index 'twitter' created successfully.")
    except RequestError as e:
        if e.error == 'resource_already_exists_exception':
            print("Index 'twitter' already exists.")
        else:
            raise

if __name__ == "__main__":
    create_twitter_index()


