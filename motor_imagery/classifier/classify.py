__author__ = 'marion'

import csv
import os
import time
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.algorithms import anomaly_likelihood
import datetime

CWD = os.path.abspath(os.getcwd())
MODEL_PARENT_DIR = os.path.join(os.path.abspath(os.path.join(CWD, os.pardir)), "training")

MODEL_PREFIX = "model"

# EEG channel names
#channels 0 and 1: right motor cortex
#channels 2 and 3: left motor cortex
CHANNELS = ["channel_0",
            "channel_1",
            "channel_2",
            "channel_3",
            ]
# motor functions that were recorded with the EEG headset
MOTOR = ["left_hand",
         "right_hand",
         "no_movement"
         ]
# set to True if you want to train on smoothed data
SMOOTH = False


def run():

    print "loading models ..."
    start = time.time()

    models = {}
    for motor in MOTOR:

        if not motor in models:
            models[motor] = {}

        for channel in CHANNELS:
            modelDir = "%s/%s_%s_%s" % (MODEL_PARENT_DIR, MODEL_PREFIX, motor, channel)
            model = ModelFactory.loadFromCheckpoint(modelDir)
            models[motor][channel] = model
            print "loaded model %s" % modelDir

    end = time.time()
    print "loaded model in % s" % (end - start)

    if SMOOTH:
        inputDataDir = "../preprocessing/smoothed_data"
    else:
        inputDataDir = "../preprocessing/formatted_data"


    # keeps track of the 3 different likelihoods per movement
    likelihoods = {}
    for motor in MOTOR:
        likelihoods[motor] = anomaly_likelihood.AnomalyLikelihood(0,1)


    for movementToClassify in MOTOR:
        for channel in CHANNELS:
            print ""
            print "Incoming EGG signal on channel %s (Patient is in the '%s' phase)" % (channel, movementToClassify)
            print "-> Let's classify this EEG signal!"

            # try with all 3 models
            averageAnomalyScores = []
            anomalyLikelihoods = []
            anomalyCount = 0
            for movement in MOTOR:

                # load model from checkpoint
                print "   * Trying with %s model : %s" % (channel, movement)
                model = models[movementToClassify][channel]
                model.enableInference({"predictedField": "channel_value"})

                # disable learning
                model.disableLearning()

                # keep tack of anomaly scores
                anomalyScores = []

                # Stream data
                inputFile = "%s/%s_%s.csv" % (inputDataDir, movement, channel)
                with open(inputFile, "rb") as input:
                    csvReader = csv.reader(input)

                    # skip 3 header rows
                    for i in range (0,3):
                        csvReader.next()

                    # stream in the data
                    rowCount = 0
                    for row in csvReader:

                        if rowCount < 100:

                            channel_value = float(row[0])
                            result = model.run({"channel_value": channel_value})
                            anomalyScore = result.inferences['anomalyScore']
                            anomalyScores.append(anomalyScore)

                            # Compute the Anomaly Likelihood
                            timestamp = datetime.datetime.now()
                            likelihood = likelihoods[movement].anomalyProbability(channel_value, anomalyScore, timestamp)
                            print "likelihood: %s" % likelihood

                            # compute the log likelihood
                            logLikelihood = likelihoods[movement].computeLogLikelihood(likelihood)
                            anomalyLikelihoods.append(logLikelihood)
                            print "loglikelihood: %s" % logLikelihood

                            # count anomalies
                            if logLikelihood > 0.9999:
                                anomalyCount += 1
                                print "anomaly count : %s " % anomalyCount


                            # just stream a bit of points
                            rowCount += 1



                print "     ... streamed %s data points" % rowCount
                averageAnomalyScore = sum(anomalyScores) / len(anomalyScores)
                averageAnomalyScores.append(averageAnomalyScore)
                print "     ... anomaly scores : %s" % anomalyScores
                print "     ... Average anomaly score : %s" % averageAnomalyScore

            # find out who had the lowest anomaly score. This is the prediction.
            # TODO: I should do that with the anomaly likelyhood instead
            minAnomalyScore = min(averageAnomalyScores)
            predictedMovement = MOTOR[averageAnomalyScores.index(minAnomalyScore)]
            print "   ==> Predicted movement : %s" % predictedMovement


if __name__ == "__main__":
  run()

