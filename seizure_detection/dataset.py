import sklearn.preprocessing

import scipy.io
import numpy as np
import sklearn.preprocessing

import matplotlib.pyplot as plt

class DataSet:
    def __init__(self, location, downsample_factor = 4):
        mat = scipy.io.loadmat(location)
        seg_name =  [k for k in mat.keys() if k not in ["__version__", '__header__', '__globals__']][0]
        if len(mat[seg_name][0][0]) == 5:
            data, data_length_sec, sampling_frequency, channels, _ = mat[seg_name][0][0]
        else:
            data, data_length_sec, sampling_frequency, channels = mat[seg_name][0][0]
        self.data_length_sec = data_length_sec
        self.sampling_frequency = sampling_frequency[0][0] / downsample_factor 
        channels_clean = []
        for c in channels[0]:
            channels_clean.append(c[0])
        self.channels = channels_clean
        down_sampled = []
        i = 0
        for row in data.T:
            i += 1
            if i % 4 == 0:
                down_sampled.append(row)
        down_sampled = np.array(down_sampled, dtype="f").T
        whitened = []
        for channel in down_sampled:
            whitened.append(sklearn.preprocessing.scale(channel))
        self.data = np.array(whitened)
    
    def dataForSeconds(self, second_start, seconds_end = None):
        i = int(second_start * self.sampling_frequency)
        if seconds_end:
            j = int(seconds_end * self.sampling_frequency)
        else:
            j = self.data.shape[1]
        return self.data.T[:][i:j].T
    
    def __str__(self):
        length = self.data.shape[1]/self.sampling_frequency
        return "Sampling frequency: %s\nDataset duration: %ss\nChannels : %s" % (self.sampling_frequency, length, self.channels)

    def plot(self, location):
        channel_count = self.data.shape[0]
        w = 60
        ma = w * self.sampling_frequency
        repeat = 6 #int(self.data.shape[1]/ma)+1
        size = (w, (channel_count+1)*repeat*2)
        nrows = (channel_count+1)*repeat
        fig, axes = plt.subplots(nrows=(channel_count+1)*repeat, ncols=1, figsize=size)
        fig.subplots_adjust(hspace=0)
        plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

        for k in range(0, repeat):
            for i in range(0, channel_count):
                axes[k*(channel_count+1) + i].plot(self.data[i][ma*k:ma*(k+1)])
                axes[k*(channel_count+1) + i].set_title(self.channels[i])
        print "save figure to %s" % location
        fig.savefig(location, bbox_inches='tight')

