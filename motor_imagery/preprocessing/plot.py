__author__ = 'marion'

import csv
import matplotlib.pylab as plt


fileName = "formatted_data/no_movement_channel_%s.csv"

# plot data
plt.figure()

for i in range(0,7):
    with open(fileName % i, 'rb') as csvFile:
        csvReader = csv.reader(csvFile)
        # skip and keep the first 3 header lines for later
        header = csvReader.next()
        unit = csvReader.next()
        stuff = csvReader.next()

        # format data for smoothing
        t = []
        x = []
        timestamp = 0
        for row in csvReader:
            x.append(float(row[0]))
            t.append(timestamp)
            timestamp +=1
        plt.plot(t,x, label="channel_%s" % i)

plt.legend()
plt.show()


