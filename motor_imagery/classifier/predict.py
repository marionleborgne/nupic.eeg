__author__ = 'marion'

import csv
import os
from nupic.frameworks.opf.modelfactory import ModelFactory
from bci.utils.nupic_output import NuPICFileOutput, NuPICPlotOutput

CWD = os.path.abspath(os.getcwd())
MODEL_PARENT_DIR = os.path.join(os.path.abspath(os.path.join(CWD, os.pardir)), "training")

MODEL_PREFIX = "model"
# EEG channel names
CHANNELS = ["channel_0",
            "channel_1",
            "channel_2",
            "channel_3",
            "channel_4",
            ]
# motor functions that were recorded with the EEG headset
MOTOR = ["no_movement",
         "left_hand",
         "right_hand"
         ]
# set to True if you want to train on smoothed data
SMOOTH = False
# Change this to switch from a matplotlib plot to file output.
PLOT = True

def run():
    if SMOOTH:
        inputDataDir = "../preprocessing/smoothed_data"
    else:
        inputDataDir = "../preprocessing/formatted_data"


    for channel in CHANNELS:
        for movement in MOTOR:

            outputName = "%s_%s" % (movement, channel)
            if PLOT:
                output = NuPICPlotOutput("output_%s" % outputName, show_anomaly_score=True)
            else:
                output = NuPICFileOutput("data_output_%s" %outputName, show_anomaly_score=True)

            # load model from checkpoint
            modelDir = "%s/%s_%s_%s" % (MODEL_PARENT_DIR, MODEL_PREFIX, movement, channel)
            model = ModelFactory.loadFromCheckpoint(modelDir)
            model.enableInference({"predictedField": "channel_value"})

            # disable learning
            model.disableLearning()

            # get input file
            inputFile = "%s/%s_%s.csv" % (inputDataDir, movement, channel)
            with open(inputFile, "rb") as input:
                csvReader = csv.reader(input)

                # skip header rows
                csvReader.next()
                csvReader.next()
                csvReader.next()

                # the real data
                timestamp = 0
                for row in csvReader:
                    channel_value = float(row[0])
                    result = model.run({"channel_value": channel_value})
                    output.write(timestamp, "channel_value", channel_value, result, prediction_step=1)
                    timestamp +=1

            output.close()


if __name__ == "__main__":
  run()

