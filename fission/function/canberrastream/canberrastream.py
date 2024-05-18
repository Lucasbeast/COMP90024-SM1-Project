from elasticsearch8 import Elasticsearch
from datetime import datetime
import logging, json, requests

def main():
    url = "https://reg.bom.gov.au/fwo/IDN60903/IDN60903.94926.json"

    response = requests.get(url)
    data = response.json()
    observations = data["observations"]["data"]
    processed_data = []

    for obs in observations:
        processed_data.append(
            {
                "air_temp": float(obs["air_temp"]),
                "apparent_t": float(obs["apparent_t"]),
                "delta_t": float(obs["delta_t"]),
                "dewpt": float(obs["dewpt"]),
                "gust_kmh": float(obs["gust_kmh"]),
                "lat": float(obs["lat"]),
                "latitude": float(obs["lat"]),
                "local_date_time_full": datetime.strptime(obs["local_date_time_full"], "%Y%m%d%H%M%S").strftime(
                    "%Y-%m-%d-%H-%M-%S"),
                "lon": float(obs["lon"]),
                "longitude": float(obs["lon"]),
                "name": "canberra",
                "press": float(obs["press"]) if obs["press"] is not None else 0.0,
                "rain_trace": float(obs["rain_trace"]) if obs["rain_trace"] != '-' else 0.0,
                "rel_hum": int(obs["rel_hum"]),
                "vis_km": float(obs["vis_km"]) if obs["vis_km"] != '-' else 0.0,
                "wind_dir": obs["wind_dir"],
                "wind_spd_kmh": float(obs["wind_spd_kmh"]),
                "wind_spd_kt": float(obs["wind_spd_kt"]),
                "wmo": int(obs["wmo"])
            }
        )

    # Elasticsearch client settings
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )

    bulk_data = []
    for item in processed_data:
        bulk_data.append(json.dumps({"index": {"_index": "bom-alias"}}))
        bulk_data.append(json.dumps(item))

    bulk_payload = "\n".join(bulk_data) + "\n"
    client.bulk(body=bulk_payload)

    return json.dumps({"status": "Completed"})

