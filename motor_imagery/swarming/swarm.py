__author__ = 'marion'

import os

CWD = os.path.abspath(os.getcwd())
MAX_VALUE = 0.0005
SWARM_CONFIG = {
  "includedFields": [
    {
      "fieldName": "channel_value",
      "fieldType": "float",
      "maxValue": MAX_VALUE ,
      "minValue": -MAX_VALUE
    }
  ],
  "streamDef": {
    "info": "data",
    "version": 1,
    "streams": [
      {
        "info": "data.csv",
        "source": "file://data.csv",
        "columns": [
          "*"
        ]
      }
    ]
  },
  "inferenceType": "TemporalAnomaly",
  "inferenceArgs": {
    "predictionSteps": [
      1
    ],
    "predictedField": "channel_value"
  },
  "swarmSize": "small"
}