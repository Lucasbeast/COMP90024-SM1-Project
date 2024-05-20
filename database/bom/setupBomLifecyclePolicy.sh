#!/bin/bash

# Read credentials
USERNAME=$(cat /etc/myapp/configs/default/shared-data/ES_USERNAME)
PASSWORD=$(cat /etc/myapp/configs/default/shared-data/ES_PASSWORD)

# Define the Lifecycle Policy
curl -X PUT "https://127.0.0.1:9200/_ilm/policy/bom_policy" -u "$USERNAME:$PASSWORD" -k \
     -H 'Content-Type: application/json' -d'
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "20GB",
            "max_age": "30d"
          }
        }
      },
      "warm": {
        "min_age": "30d",
        "actions": {
          "allocate": {
            "number_of_replicas": 1,
            "include": {},
            "exclude": {},
            "require": {"box_type": "warm"}
          }
        }
      },
      "cold": {
        "min_age": "90d",
        "actions": {
          "freeze": {}
        }
      },
      "delete": {
        "min_age": "120d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
'

# Apply Lifecycle Policy to the Index Template
curl -X PUT "https://127.0.0.1:9200/_template/bom_template" -u "$USERNAME:$PASSWORD" -k \
     -H 'Content-Type: application/json' -d'
{
  "index_patterns": ["bom-*"],
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "index.lifecycle.name": "bom_policy",
    "index.lifecycle.rollover_alias": "bom"
  }
}
'

# Set alias for the existing index
curl -X POST "https://127.0.0.1:9200/_aliases" -u "$USERNAME:$PASSWORD" -k \
  -H 'Content-Type: application/json' -d'
{
  "actions": [
    {
      "add": {
        "index": "bom",
        "alias": "bom-alias",
        "is_write_index": true
      }
    }
  ]
}'

# Update index settings to use lifecycle policy and rollover alias
curl -X PUT "https://127.0.0.1:9200/bom/_settings" -u "$USERNAME:$PASSWORD" -k \
  -H 'Content-Type: application/json' -d'
{
  "index": {
    "lifecycle.name": "bom_policy",
    "lifecycle.rollover_alias": "bom-alias"
  }
}'




