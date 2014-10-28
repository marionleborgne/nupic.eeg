__author__ = 'marion'

import csv
import smooth

""""
Split the inital motor imagery dataset into 3 dataset.
One dataset for each phase:
- if label is "-1" then the subject is thinking about moving his LEFT hand
- if label is "1" then the subject is thinking about moving his RIGHT hand
- if label is "0" then the subject is NOT THINKING about moving any part of the body
"""

# load file with EEG motor imagery recordings
fileName = "original_data/motor_data_tomas.csv"
inputFile = open(fileName, 'rb')
csvReader = csv.reader(inputFile)

# EEG channels
channels = ["channel_0",
            "channel_1",
            "channel_2",
            "channel_3",
            "channel_4",
            "channel_5",
            "channel_6",
            "channel_7"]

# skip first row
csvReader.next()

# labels
labels = []
labels.append("left_hand")
labels.append("right_hand")
labels.append("no_movement")

# labels keys in EEG dataset
labelsMap = {}
labelsMap["-1"] = "left_hand"
labelsMap["1"] = "right_hand"
labelsMap["0"] = "no_movement"


# data headers
sampled_data = {}
for label in labels:
    for channel in channels:
        key = "%s_%s" % (label, channel)
        sampled_data[key] = []
        sampled_data[key] = []
        # add header
        header = []
        header.append("channel_value")
        sampled_data[key].append(header)
        # add unit for nupic
        unit = []
        unit.append("float")
        sampled_data[key].append(unit)
        # timestamp stuff that won't be useful in this case so it's set to ""
        timestamp = []
        timestamp.append("")
        sampled_data[key].append(timestamp)




# Data re-sampling :
# original data has a sampling rate of 4ms
sampling_rate = 5
rowCount = 0
for rawRow in csvReader:

    if rowCount % sampling_rate == 0:
        labelValue = rawRow[-1]
        label = labelsMap[labelValue]

        # The last column is the label.
        # The second to last column is the timestamp.
        # We don't want to have the fields timestamp or label in the new dataset,
        # so we remove these fields
        row = rawRow[:-2]
        for i in range(len(row)):
            channel = channels[i]
            key = "%s_%s" % (label, channel)
            newRow = []
            newRow.append(float(row[i]))
            sampled_data[key].append(newRow)

    rowCount += 1



for label in labels:
    for channel in channels:
        key = "%s_%s" % (label, channel)
        fileName = "formatted_data/%s.csv" % key
        with open(fileName, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(sampled_data[key])