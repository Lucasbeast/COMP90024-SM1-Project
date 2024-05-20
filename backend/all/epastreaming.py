import requests
from elasticsearch8 import Elasticsearch, helpers
import warnings
import json

warnings.filterwarnings("ignore")


def main():
    # API call to fetch data
    url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/parameters?environmentalSegment=air"
    headers = {
        'Cache-Control': 'no-cache',
        'X-API-Key': 'ff68e5cb354b420e97a3752fd4ae3630',
        'User-Agent': 'PostmanRuntime/7.28.4'
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse JSON data

        # Initialize the Elasticsearch client
        es = Elasticsearch(
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs=False,
            ssl_show_warn=False,
            basic_auth=('elastic', 'elastic'))

        # Prepare data for bulk indexing
        actions = []

        if "records" in data:
            for record in data["records"]:
                doc = {
                    "_index": "epa-alias",
                    "_source": {
                        "siteID": record["siteID"],
                        "siteName": record["siteName"],
                        "longitude": record["geometry"]["coordinates"][0],
                        "latitude": record["geometry"]["coordinates"][1],
                        "parameters": []
                    }
                }

                for param in record.get("parameters", []):
                    for series in param.get("timeSeriesReadings", []):
                        for reading in series.get("readings", []):
                            doc["_source"]["parameters"].append({
                                "name": param["name"],
                                "timeSeriesName": series["timeSeriesName"],
                                "startDateTime": reading.get("since", "Unknown time"),
                                "untilDateTime": reading.get("until", "Unknown time"),
                                "averageValue": reading.get("averageValue", 0),  # Default to 0 if not present
                                "unit": reading.get("unit", "Unknown unit"),
                                "totalSample": reading.get("totalSample", 0)  # Default to 0 if not present
                            })

                actions.append(doc)

        # Perform bulk indexing
        if actions:
            helpers.bulk(es, actions)
            print(f"Successfully indexed {len(actions)} records")
            return json.dumps({"success": "win"})
        else:
            print("No data to index")

    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
