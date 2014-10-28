__author__ = 'marion'


MSMODIFIER = 1000

import csv
import time
import numpy
import pylab
import matplotlib.pyplot as plt


def smooth(x,beta, window_len):
 """ kaiser window smoothing """
 # extending the data at beginning and at the end
 # to apply the window at the borders
 s = numpy.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]
 w = numpy.kaiser(window_len,beta)
 y = numpy.convolve(w/w.sum(), s, mode='valid')
 offset = window_len/2
 return y[offset:len(y)-offset]


# different zooming configuration of the GUI
zoom_ui = [ 'raw','hour','day', 'month', 'year']

# time window
win = {}
win['raw'] = 10 # 1 data point every 10 s
win['hour'] = 60 # data point every 60 s
win['day'] = 5 * 60 # data point every 5 minutes (300 s)
win['month'] =  60 * 60 # 1 data point every hour
win['year'] = 365 * 24 * 60 * 60 # 1 data point every day

t = {}  # resampled time scale
x = {}  # resampled data
x_filtered = {}  # filtered data

# sampling rate
r = {}
for p in zoom_ui:
    r[p] = 1 / win[p]

def resample_data():

    for p in zoom_ui[1:]:

        t[p] = []
        x[p] = []
        w = win[p] / win['raw']
        x_resampled = x[p]
        t_resampled = t[p]
        for i in xrange(0, len(t['raw'])/w-1):
            acc = 0
            for j in xrange(0, w):
                acc += x['raw'][i*w+j]/w
            x_resampled.append(acc)
            t_resampled.append(t['raw'][(i+1)*w])

if __name__ == "__main__" :


    csvFile = open("../preprocessing/formatted_data/no_movement_channel_0.csv")
    csvReader = csv.reader(csvFile)

    # skip the first 3 lines
    header = csvReader.next()
    unit = csvReader.next()
    stuff = csvReader.next()


    t['raw'] = []
    timestamp = 0
    x['raw'] = []
    for row in csvReader:
        x['raw'].append(float(row[0]))
        t['raw'].append(timestamp)
        timestamp +=1

    resample_data()

    # smoothing the data with kaiser window smoothing
    window_len = 7 # window lenght
    b = 20
    beta = [5,16]
    pylab.figure(1)
    pylab.plot(t['raw'], x['raw'],label="original signal (1 data point every 4 ms)",alpha=.3)

    for p in zoom_ui[1:-2]:
        #plt.step(t[p], x[p],label="original signal resampled ( 1 / "+str(win[p])+" )" )
        print x[p]
    for p in zoom_ui[0:-2]:
        x_filtered[p] = smooth(x[p],b,window_len)

        print "t", len(t[p])
        print "x_filtered", len( x_filtered[p] )
        pylab.plot(t[p], x_filtered[p],label="filtered data ( sampling rate = 1 / "+str(win[p])+" )")
    pylab.legend()
    pylab.show()

    filteredDataFile = "smoothed_data/smoothed_no_movement_channel_0.csv"
    dataToSave = []
    dataToSave.append(header)
    dataToSave.append(unit)
    dataToSave.append(stuff)
    for point in x_filtered['raw']:
        data = []
        data.append(point)
        dataToSave.append(data)

    with open(filteredDataFile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(dataToSave)

