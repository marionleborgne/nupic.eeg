__author__ = 'marion'

import numpy
import csv
import pylab

def smooth(x,beta, window_len):
    """
    Kaiser window smoothing.
    Increasing beta widens the main lobe and decreases
    the amplitude of the sidelobes (i.e., increases the attenuation).
    Note: widening the main lobe reduces frequency resolution.
    """
    # extending the data at beginning and at the end
    # to apply the window at the borders
    s = numpy.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]
    w = numpy.kaiser(window_len,beta)
    y = numpy.convolve(w/w.sum(), s, mode='valid')
    offset = window_len/2
    return y[offset:len(y)-offset]


csvFile = open("formatted_data/no_movement_channel_0.csv")
csvReader = csv.reader(csvFile)

# skip and keep the first 3 header lines for later
header = csvReader.next()
unit = csvReader.next()
stuff = csvReader.next()

# format data for smoothing
t = []
timestamp = 0
x = []
for row in csvReader:
    x.append(float(row[0]))
    t.append(timestamp)
    timestamp +=1


# smooth the data by convoling it with a kaiser window
window_len = 81
b = 20
beta = [5,16]
x_filtered = smooth(x,b,window_len)


# plot data
pylab.figure(1)
pylab.plot(t, x,label="original signal)",alpha=.3)
pylab.plot(t, x_filtered,label="filtered data")
pylab.legend()
#pylab.show()


# create new dataset with filtered data
dataToSave = []
dataToSave.append(header)
dataToSave.append(unit)
dataToSave.append(stuff)
for point in x_filtered:
    data = []
    data.append(point)
    dataToSave.append(data)

# save data to file
filteredDataFile = "smoothed_data/smoothed_no_movement_channel_0.csv"
with open(filteredDataFile, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(dataToSave)