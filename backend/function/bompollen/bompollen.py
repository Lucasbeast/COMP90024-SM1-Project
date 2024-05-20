
from elasticsearch8 import Elasticsearch
from datetime import datetime
import json
import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def prediction(url, name):
    response = requests.get(url)
    data = response.json()
    observations = data["observations"]["data"]
    bom_data_new = []

    for obs in observations:
        bom_data_new.append(
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
                "name": name,
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

    client = Elasticsearch(
        # ['https://127.0.0.1:9200'],
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )

    es_response = client.search(index="bom-alias", body={"query": {"match": {"name": name}}}, size=500)

    bom_old_df = [{
        "local_date_time_full": datetime.strptime(hit["_source"]["local_date_time_full"], "%Y-%m-%d-%H-%M-%S").strftime(
            "%m-%d"),
        "name": hit["_source"]["name"],
        "air_temp": hit["_source"]["air_temp"],
        "apparent_t": hit["_source"]["apparent_t"],
        "dewpt": hit["_source"]["dewpt"],
        "gust_kmh": hit["_source"]["gust_kmh"],
        "rel_hum": hit["_source"]["rel_hum"],
        "wind_spd_kmh": hit["_source"]["wind_spd_kmh"],
    } for hit in es_response['hits']['hits']]

    es_pollen_response = client.search(index="pollen", body={"query": {"match": {"area": name}}}, size=500)
    pollen_list = [{
        "start_date": datetime.strptime(hit["_source"]["start_date"], "%Y-%m-%d").strftime("%m-%d"),
        "end_date": datetime.strptime(hit["_source"]["end_date"], "%Y-%m-%d").strftime("%m-%d"),
        "area": hit["_source"]["area"],
        "pollen_total": hit["_source"]["poaceae_pollen"] + hit["_source"]["other_pollen"],
    } for hit in es_pollen_response['hits']['hits']]

    bom_df = pd.DataFrame(bom_old_df)
    pollen_df = pd.DataFrame(pollen_list)

    def is_within_range(date, start_date, end_date):
        return start_date <= date <= end_date

    merged_list = []
    for bom in bom_df.itertuples():
        for pollen in pollen_df.itertuples():
            if bom.name == pollen.area and is_within_range(bom.local_date_time_full, pollen.start_date, pollen.end_date):
                merged_list.append({
                    "local_date_time_full": bom.local_date_time_full,
                    "name": bom.name,
                    "air_temp": bom.air_temp,
                    "apparent_t": bom.apparent_t,
                    "dewpt": bom.dewpt,
                    "gust_kmh": bom.gust_kmh,
                    "rel_hum": bom.rel_hum,
                    "wind_spd_kmh": bom.wind_spd_kmh,
                    "pollen_total": pollen.pollen_total
                })

    merged_df = pd.DataFrame(merged_list)

    X = merged_df[['air_temp', 'apparent_t', 'dewpt', 'gust_kmh', 'rel_hum', 'wind_spd_kmh']]
    y = merged_df['pollen_total']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    bom_new_df = pd.DataFrame(bom_data_new)
    X_new = bom_new_df[['local_date_time_full', 'air_temp', 'apparent_t', 'dewpt', 'gust_kmh', 'rel_hum', 'wind_spd_kmh']]
    X_new_features = X_new[['air_temp', 'apparent_t', 'dewpt', 'gust_kmh', 'rel_hum', 'wind_spd_kmh']]
    y_pred = model.predict(X_new_features)
    prediction_df = pd.DataFrame({
        'local_date_time_full': X_new['local_date_time_full'],
        'air_temp': X_new['air_temp'],
        'apparent_t': X_new['apparent_t'],
        'dewpt': X_new['dewpt'],
        'gust_kmh': X_new['gust_kmh'],
        'rel_hum': X_new['rel_hum'],
        'wind_spd_kmh': X_new['wind_spd_kmh'],
        'pollen_total': y_pred
    })

    def format_row(row):
        return {
            'location': name,
            'local_date_time_full': row['local_date_time_full'],
            'air_temp': row['air_temp'],
            'apparent_t': row['apparent_t'],
            'dewpt': row['dewpt'],
            'gust_kmh': row['gust_kmh'],
            'rel_hum': row['rel_hum'],
            'wind_spd_kmh': row['wind_spd_kmh'],
            'pollen_total': row['pollen_total']
        }

    prediction = prediction_df.apply(format_row, axis=1).tolist()
    json_data = json.dumps(prediction, ensure_ascii=False, indent=4)
    return json_data

def main():
    try:
        data = requests.get_json()
        name = data.get('name')
    except (KeyError, TypeError):
        return json.dumps({'error': 'Name parameter is missing in the request body'}), 400
    if name == "campbelltown":
        url = "https://reg.bom.gov.au/fwo/IDN60901/IDN60901.94757.json"
    elif name == "canberra":
        url = "https://reg.bom.gov.au/fwo/IDN60903/IDN60903.94926.json"
    elif name == "parkville":
        url = "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json"
    elif name == "rocklea":
        url = "https://reg.bom.gov.au/fwo/IDQ60901/IDQ60901.94576.json"
    predictions = prediction(url,name)
    return predictions



