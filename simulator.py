import time, threading, random
import numpy as np
#import scipy as sp
import os
import cv2
import timeit
import json
import string
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
    binning = int(request.form["binning"])
    color_channel = request.form.getlist("color_channel")
    connect_kafka = request.form["kafka"]
    interval = float(frequency)
    get_files(file_path, interval, binning, color_channel, connect_kafka)
    return "You are now streaming file names with Kafka"


def get_files(file_path, frequency, binning, color_channel, connect_kafka):

    for root, dirs, files in os.walk(file_path):
        if not files:
            pass
        else:
            if not dirs:
                pass
            for i in range(len(files)):
                get_file(files, i, color_channel, file_path, binning, connect_kafka)
                time.sleep(frequency)


def get_file(files, i, color_channel, file_path, binning, connect_kafka):
    if files[i][-5] in color_channel:
        img = cv2.imread(file_path + files[i], -1)
        binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
        if connect_kafka == "yes":
            ret, jpeg = cv2.imencode('.png', img_as_ubyte(binned_img))
            kafka_producer.connect(jpeg.tobytes())


@app.route("/adminPanel")
def admin():
    return render_template("admin_panel.html")



# def admin_fun():

#     for run in run_information:
#         #start a new test run and save score
#         #use timeit
#         file_path = run_information[run]['file_path']
#         print(file_path)
#         files = os.listdir(file_path)
#         print(files)
#         color_channel = run_information[run]['color_channel']
#         binning = run_information[run]['binning']
#         connect_kafka = run_information[run]['connect_kafka']
#         setup = '''
# from __main__ import run_information
# file_path = run_information[run]['file_path']
# print(file_path)
# files = os.listdir(file_path)

# #connect_kafka = run_information[run]['connect_kafka']
#         '''
#         for i in range(100):
#             timeit.timeit('get_file(files, i, color_channel, file_path, binning, connect_kafka)',
#                           setup=setup,
#                           number=10)
#             #get_file(files, i, color_channel, file_path, binning, connect_kafka)
#
#         result = run_information[run]
#         result = json.dumps(result)
#         save_results(result)
#
#
#     #output: 1. text file with freq info 2. graphs showing performance
#
#     return ("in admin fun")
def admin_fun():
    #test max freq - kolla hur lång tid varje steg i for-loopen tar
    #test if set freq corresponds to actual freq
    #test freq for different image sizes

    # input: JSON file with test settings (possible to make multiple runs at once)
    json_file = request.form["file_path"]
    json_file = open(json_file, "r")
    run_information = json_file.read()
    run_information = json.loads(run_information)

    return run_information


def inner_func(run_info):
    print(run_info)


@app.route("/adminPanel", methods=['POST'])
def test_timeit():
    setup_template = '''
from simulator import admin_fun, inner_func, get_files
run_information = admin_fun() 
frequency = run_information['run']['frequency']
color_channel = run_information['run']['color_channel']
binning = run_information['run']['binning']
file_path = run_information['run']['file_path']
connect_kafka = run_information['run']['connect_kafka']   
    '''

    runs = 2
    for run in range(1, runs):
        setup = setup_template.replace("'run'", "'run{}'".format(run))
        save_results(str(timeit.timeit('get_files(file_path, frequency, binning, color_channel, connect_kafka)',
                                       setup=setup, number=3)), run)
    return "test ready"


def save_results(results, run):
    fo = open("result.txt", "a")
    fo.write("Run nr, result: {} ".format(run))
    fo.write(results)
    fo.write("\n")
    fo.close()


def retrieval_time():
    #kolla hur lång tid varje steg i (inre) for-loopen tar för att hämta bilder
    #output: medelvärde, std, var, histogram över alla frekvenser
    #1. set freq = 0
    pass


if __name__ == "__main__":
    app.run(debug=True)
