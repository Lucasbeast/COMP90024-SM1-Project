from flask import Flask, request, jsonify
from elasticsearch8 import Elasticsearch

app = Flask(__name__)


# this function build connection with db
def query_es(body, index_name):
    client = Elasticsearch(
        'https://localhost:9200',
        basic_auth=("elastic", "elastic"),
        verify_certs=False,
        ssl_show_warn=False
    )
    response = client.search(body=body, index=index_name)
    return response['hits']['hits']


@app.route('/query-es', methods=['GET'])
def main():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON body found"}), 400

    body = data.get('body')
    index_name = data.get('index')
    if not body or not index_name:
        return jsonify({"error": "Missing body or index parameter"}), 400

    try:
        results = query_es(body, index_name)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
