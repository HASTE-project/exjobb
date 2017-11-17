import time, random
import numpy as np
import os
import cv2
import timeit
import json
import kafka_producer

from skimage import img_as_ubyte
from skimage.measure import block_reduce


def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))


def get_files(file_path, frequency, binning, color_channel, connect_kafka):
    print('in get files')
    files = os.listdir(file_path)
    for file in files:
        if os.path.isfile(file_path + file):
            get_file(file, color_channel, file_path, binning, connect_kafka)
        time.sleep(frequency)


def get_file(file, color_channel, file_path, binning, connect_kafka):
    print('in get file simNoFlask')
    if file[-5] in color_channel:
        print('color channel ok')
        img = cv2.imread(file_path + file, -1)
        binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
        if connect_kafka == "yes":
            print('kafka conncent')
            ret, jpeg = cv2.imencode('.tif', img_as_ubyte(binned_img))
            kafka_producer.connect(jpeg.tobytes())


 
