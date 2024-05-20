#!/bin/bash

# Read credentials from files
USERNAME=$(cat /etc/myapp/configs/default/shared-data/ES_USERNAME)
PASSWORD=$(cat /etc/myapp/configs/default/shared-data/ES_PASSWORD)

curl -X PUT -k 'https://127.0.0.1:9200/pollen' \
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
               "id": {
                   "type": "keyword"
               },
               "area": {
                   "type": "keyword"
               },
               "poaceae_pollen": {
                   "type": "integer",  
                   "null_value": 0  
               },
               "other_pollen": {
                   "type": "integer",  
                   "null_value": 0  
               },
               "longitude": {
                   "type": "float"  
               },
               "latitude": {
                   "type": "float"  
               },
              "start_date": {
                   "type": "date",
                   "format": "yyyy-MM-dd"
               },
               "end_date": {
                   "type": "date",
                   "format": "yyyy-MM-dd"
               }
           }
       }
   }' \
    --user "$USERNAME:$PASSWORD" | jq '.'
