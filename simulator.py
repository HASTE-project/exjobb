import time, threading, random
import numpy as np
#import scipy as sp
import os
import cv2
import timeit
#import kafka_producer
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
        #print("Length of 'files': {}", len(files))
        if not files:
            pass
            #print("files is empty")
        else:
            if not dirs:
                pass #   print("dirs is empty")
            #print(file_path + files[0])
            for i in range(len(files)):
                get_file(files, i, color_channel, file_path, binning, connect_kafka)
                # if files[i][-5] in color_channel:
                #   #  print("i = {}".format(i))
                #     img = cv2.imread(file_path + files[i], -1)
                #     binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                #     if connect_kafka == "yes":
                #         #print("in if")
                #         ret, jpeg = cv2.imencode('.png', img_as_ubyte(binned_img))
                #         kafka_producer.connect(jpeg.tobytes())
                time.sleep(frequency)


def get_file(files, i, color_channel, file_path, binning, connect_kafka):
    if files[i][-5] in color_channel:
        #  print("i = {}".format(i))
        img = cv2.imread(file_path + files[i], -1)
        binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
        if connect_kafka == "yes":
            # print("in if")
            ret, jpeg = cv2.imencode('.png', img_as_ubyte(binned_img))
            kafka_producer.connect(jpeg.tobytes())


@app.route("/adminPanel")
def admin():
    return render_template("admin_panel.html")


@app.route("/adminPanel", methods=['POST'])
def admin_fun():
    print("in admin fun")
    #test max freq - kolla hur lång tid varje steg i for-loopen tar
    #test if set freq corresponds to actual freq
    #test freq for different image sizes

    #input: JSON file with test settings (possible to make multiple runs at once)
    #output: 1. text file with freq info 2. graphs showing performance
    timeit.timeit(get_files(file_path, frequency, binning,
                            color_channel, connect_kafka),
                  '''from __main__ import get_files,'
                    'file_path, frequency=0, color_channel,'
                    'binning, connect_kafka''')
    # (stmt='pass', setup='pass', timer=<default timer>, number=1000000, globals=None)


def retrieval_time():
    #kolla hur lång tid varje steg i (inre) for-loopen tar för att hämta bilder
    #output: medelvärde, std, var, histogram över alla frekvenser
    #1. set freq = 0
    pass


if __name__ == "__main__":
    app.run(debug=True)
