import time, threading, random
import numpy as np
#import scipy as sp
import os
import cv2
import kafka_producer
from skimage import img_as_ubyte

from skimage.measure import block_reduce
from os.path import join, getsize
from flask import Flask, Response, render_template, request

app = Flask(__name__)


def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))


@app.route("/fileWalk")
def file_walk():
    return render_template('file_walk_page.html')


@app.route("/fileWalk", methods=['POST'])
def file_walk_post():
    file_path = request.form["file_path"]
    frequency = request.form["interval"]
    binning = request.form["binning"]
    color_channel = request.form.getlist("color_channel")
    connect_kafka = request.form["kafka"]
    interval = float(frequency)
    get_files(file_path, interval, binning, color_channel, connect_kafka)
    return "You are now streaming file names with Kafka"


def get_files(file_path, frequency, binning, color_channel, connect_kafka):
    print("freq: {} binning: {} color_channels: {} ".format(frequency, binning, color_channel))
    print("in get_files")
    binning = int(binning)
    frequency = float(frequency)

    for root, dirs, files in os.walk(file_path):
        print("Length of 'files': {}", len(files))
        if not files:
            print("files is empty")
        else:
            if not dirs:
                print("dirs is empty")
            print(file_path + files[0])
            for i in range(len(files)):
                if files[i][-5] in color_channel:
                    print("i = {}".format(i))
                    img = cv2.imread(file_path + files[i], -1)
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        #print("in if")
                        ret, jpeg = cv2.imencode('.png', img_as_ubyte(binned_img))
                        kafka_producer.connect(jpeg.tobytes())
                    time.sleep(frequency)


if __name__ == "__main__":
    app.run(debug=True)
