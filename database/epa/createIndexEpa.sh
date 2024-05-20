#!/bin/bash

# Read credentials from files
USERNAME=$(cat /etc/myapp/configs/default/shared-data/ES_USERNAME)
PASSWORD=$(cat /etc/myapp/configs/default/shared-data/ES_PASSWORD)

curl -X PUT -k "https://127.0.0.1:9200/epa-000001" \
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
              "siteID": {
                  "type": "keyword"
              },
              "siteName": {
                  "type": "text"
              },
              "longitude": {
                  "type": "float"
              },
              "latitude": {
                  "type": "float"
              },
              "parameters": {
                  "type": "nested",
                  "properties": {
                      "name": {
                          "type": "keyword"
                      },
                      "timeSeriesName": {
                          "type": "keyword"
                      },
                      "startDateTime": {
                          "type": "date"
                      },
                      "untilDateTime": {
                          "type": "date"
                      },
                      "averageValue": {
                          "type": "float"
                      },
                      "unit": {
                          "type": "keyword"
                      },
                      "totalSample": {
                          "type": "integer"
                      }
                  }
              }
          }
      }
    }' \
    --user "$USERNAME:$PASSWORD" | jq '.'