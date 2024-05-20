#!/bin/bash

# Read credentials from files
USERNAME=$(cat /etc/myapp/configs/default/shared-data/ES_USERNAME)
PASSWORD=$(cat /etc/myapp/configs/default/shared-data/ES_PASSWORD)

# Execute the curl command using the credentials
curl -X PUT -k 'https://127.0.0.1:9200/sensor' \
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
               "date": {
                   "type": "date",
                   "format": "yyyy-MM-dd"
               },
               "time": {
                   "type": "text"
               },
               "dev_id": {
                   "type": "keyword"
               },
               "temperature": {
                   "type": "float"
               },
               "humidity": {
                   "type": "float"
               },
               "battery": {
                   "type": "short"
               },
               "location": {
                   "type": "geo_point"
               }
           }
       }
   }' \
   --user "$USERNAME:$PASSWORD" | jq '.'