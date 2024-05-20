from flask import request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from elasticsearch8 import Elasticsearch

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))


def es_into_dict(es_outcome: list):
    data = []
    for document in es_outcome:
        if '_source' in document:
            data.append(document['_source'])
    return data


lemmatizer = WordNetLemmatizer()


def preprocess(text):
    tokens = word_tokenize(text)
    return ' '.join(
        [lemmatizer.lemmatize(word.lower()) for word in tokens if word.isalpha() and word.lower() not in stop_words])


def fetch_data(body):
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        basic_auth=("elastic", "elastic"),
        verify_certs=False,
        ssl_show_warn=False
    )
    response = client.search(body=body, index='twitter-word')
    return es_into_dict(response['hits']['hits'])


def count_words(text):
    words = word_tokenize(text)
    word_freq = {}
    for word in words:
        word_lower = word.lower()
        if word_lower not in stop_words:
            word_freq[word_lower] = word_freq.get(word_lower, 0) + 1
    return word_freq


def main():
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    try:
        # handle some special cases
        if year not in [2021, 2022]:
            return 'Invalid year'
        if month > 12 or month < 1:
            return 'Invalid month'
        if year == 2021:
            if month < 6:
                return 'no data available, please try other months'
        if year == 2022:
            if month > 7:
                return 'no data available, please try other months'

        # Format the start and end dates for the month
        start_date = f"{year}-{month:02d}-01T00:00:00Z"
        end_date = f"{year}-{month:02d}-31T23:59:59Z"

        query = {
            "size": 1000,
            "query": {
                "range": {
                    "created_at": {
                        "gte": start_date,
                        "lte": end_date,
                        "format": "strict_date_optional_time"
                    }
                }
            }
        }

        # Fetch data from Elasticsearch
        data = fetch_data(query)

        # Combine all text data and preprocess
        all_text = ' '.join(preprocess(doc['text']) for doc in data if 'text' in doc)

        # Count words
        word_count = count_words(all_text)

        # Return the word frequency dictionary
        return jsonify(word_count)

    except Exception as e:
        return jsonify({'error': str(e)}), 400
