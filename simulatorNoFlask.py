"""
Simulator program to simulate a microscope by setting frequency, binning and color channel. The simulator
can be attached to a streaming framework, at the moment Apache Kafka.

The simulator is started by calling:
simulatorNoFlask.get_files(file_path, frequency, binning, color_channel, connect_kafka)
file_path: where the image files are stored period: the period time between each image. The maximum
speed allowed by the system is retrieved when setting period to 0. binning: change image's binning to decrease
message size color_channel: set which color_channels to include, there are up to five channels (1-5), they are set by
giving a list, for example ['1','3'] sets color_channels 1 and 3.
connect_kafka: set to "yes" is Kafka is used as a streaming framework.
"""

import os
import sys
import time

import cv2
import numpy as np
from skimage import img_as_uint
from skimage.measure import block_reduce

import kafka_producer


def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))


def get_files(file_path, period, binning, color_channel, connect_kafka):
    """This function retrieves files and creates a stream of files to be used as a microscope simulator."""
    files = os.listdir(file_path)
    for file in files:
        if os.path.isfile(file_path + file):
            get_file(file, color_channel, file_path, binning, connect_kafka)
        time.sleep(period)


def get_file(file, color_channel, file_path, binning, connect_kafka):
    """
    This function takes one file, checks if it has the correct color channel, reads and converts the file and
    sends it to the streaming framework.
     """
    if file[-5] in color_channel:
        img = cv2.imread(file_path + file, -1)
        binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
        if connect_kafka == "yes":
            ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img)) # convert image file so it can be streamed
            print("size: {}".format(sys.getsizeof(jpeg.tobytes())))
            print(file)
            kafka_producer.connect(jpeg.tobytes())
