#!/usr/bin/python

import csv
import os
from bci.swarming.model_params.model_params import MODEL_PARAMS
from nupic.frameworks.opf.modelfactory import ModelFactory

CWD = os.path.abspath(os.getcwd())
MODEL_PREFIX = "model"
# EEG channel names
CHANNELS = ["channel_0",
            "channel_1",
            "channel_2",
            "channel_3",
            "channel_4",
            "channel_5",
            "channel_6",
            "channel_7"]
# motor functions that were recorded
MOTOR = ["no_movement",
         "left_hand",
         "right_hand"]
# set to True if you want to train on smoothed data
SMOOTH = False


def run():
    if SMOOTH:
        inputDataDir = "../preprocessing/smoothed_data"
    else:
        inputDataDir = "../preprocessing/formatted_data"

    model = ModelFactory.create(MODEL_PARAMS)
    model.enableInference({"predictedField": "channel_value"})

    for channel in CHANNELS:
        for movement in MOTOR:

            inputFile = "%s/%s_%s.csv" % (inputDataDir, movement, channel)
            with open(inputFile, "rb") as input:
                csvReader = csv.reader(input)

                # skip header rows
                csvReader.next()
                csvReader.next()
                csvReader.next()

                # train model
                for row in csvReader:
                  channel_value = float(row[0])
                  model.run({"channel_value": channel_value})

                # save model
                modelDir = "%s/%s_%s_%s" % (CWD, MODEL_PREFIX, movement, channel)
                model.save(modelDir)
                print "Saved new model in %s" % modelDir


if __name__ == "__main__":
  run()
