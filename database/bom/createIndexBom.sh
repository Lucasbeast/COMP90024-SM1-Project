#!/bin/bash

# Read credentials from files
USERNAME=$(cat /etc/myapp/configs/default/shared-data/ES_USERNAME)
PASSWORD=$(cat /etc/myapp/configs/default/shared-data/ES_PASSWORD)

# Execute the curl command using the credentials
curl -X PUT -k 'https://127.0.0.1:9200/bom-000001' \
     --header 'Content-Type: application/json' \
     --data '{
       "settings": {
           "index": {
               "number_of_shards": 3,
               "number_of_replicas": 1
           }
       },
       "mappings": {
           "properties": {
               "header_ID": {
                   "type": "keyword"
               },
               "sort_order": {
                   "type": "keyword"
               },
               "wmo": {
                   "type": "integer"
               },
               "name": {
                   "type": "text"
               },
               "local_date_time_full": {
                   "type": "date",
                   "format": "yyyyMMddHHmmss"
               },
               "lat": {
                   "type": "float"
               },
               "lon": {
                   "type": "float"
               },
               "apparent_t": {
                   "type": "float"
               },
               "delta_t": {
                   "type": "float"
               },
               "gust_kmh": {
                   "type": "float"
               },
               "air_temp": {
                   "type": "float"
               },
               "dewpt": {
                   "type": "float"
               },
               "press": {
                   "type": "float"
               },
               "rain_trace": {
                   "type": "float"
               },
               "rel_hum": {
                   "type": "integer"
               },
               "vis_km": {
                   "type": "float"
               },
               "wind_dir": {
                   "type": "text"
               },
               "wind_spd_kmh": {
                   "type": "float"
               },
               "wind_spd_kt": {
                   "type": "float"
               }
           }
       }
   }' \
   --user "$USERNAME:$PASSWORD" | jq '.'

