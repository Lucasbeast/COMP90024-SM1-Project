from flask import Flask, request, jsonify
from elasticsearch8 import Elasticsearch

app = Flask(__name__)


def query_es(body, index_name):
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        http_auth=("elastic", "elastic"),
        verify_certs=False,
        ssl_show_warn=False
    )

    response = client.search(body=body, index=index_name)
    return response['hits']['hits']


@app.route('/query_es', methods=['POST'])
def get_es_data():
    data = request.get_json()
    body = data.get('body')
    index_name = data.get('index')
    if body and index_name:
        try:
            results = query_es(body, index_name)
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Missing body or index parameter"}), 400
