import time, threading, random
import numpy as np
#import scipy as sp
import os

import cv2


from skimage.measure import block_reduce
from os.path import join, getsize
from flask import Flask, Response, render_template, request

app = Flask(__name__)


@app.route("/index")
def index():
    return render_template('start_page.html')


@app.route("/index", methods=['POST'])
def index_post():
    frequency = request.form["interval"]
    binning = request.form["binning"]
    color_channel = request.form.getlist("color_channel")
    interval = float(frequency)
    print("binning: {} color_channel: {}".format(binning, color_channel))
    main(interval, binning, color_channel)
    return "You are now writing to test.txt every {} second.".format(frequency)


def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))


def main(freq, binning, color_channel):
    interval = random.uniform(freq - freq / 5, freq - freq / 5)
    #  binned_image = block_reduce(image, block_size=(binning, binning, 1), func=np.sum)
    threading.Timer(interval, main, [freq]).start()


@app.route("/fileWalk")
def file_walk():
    return render_template('file_walk_page.html')


@app.route("/fileWalk", methods=['POST'])
def file_walk_post():
    file_path = request.form["file_path"]
    frequency = request.form["interval"]
    binning = request.form["binning"]
    color_channel = request.form.getlist("color_channel")
    interval = float(frequency)
    print("binning: {} color_channel: {}".format(binning, color_channel))
    get_files(file_path, frequency, binning, color_channel)
    return "You are now streaming file names with Kafka"


def get_files(file_path, frequency, binning, color_channel):
    print("freq: {} binning: {} color_channels: {} ".format(frequency, binning, color_channel))
    print("in get_files")
    binning = int(binning)
    frequency = float(frequency)
    print(file_path)
    if isinstance(binning, str):
        print("binning is string")

    for root, dirs, files in os.walk(file_path):
        print("Length of 'files': {}", len(files))
        if not files:
            print("files is empty")
        else:
            if not dirs:
                print("dirs is empty")
            print(file_path + files[0])
            for i in range(len(files)):
                print("i = {}".format(i))
                img = cv2.imread(file_path + files[i], -1)

                binned_img = block_reduce(img, block_size=(1, 1), func=np.sum)
            #    ret, jpeg = cv2.imencode('.png', binned_img)
                time.sleep(frequency)


if __name__ == "__main__":
    app.run(debug=True)
