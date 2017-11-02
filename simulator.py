import time, threading, random
import numpy as np
#import scipy as sp
import os
import cv2
import timeit
import json
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



# def admin_fun():
#     #test max freq - kolla hur lång tid varje steg i for-loopen tar
#     #test if set freq corresponds to actual freq
#     #test freq for different image sizes
#
#     # input: JSON file with test settings (possible to make multiple runs at once)
#     json_file = request.form["file_path"]
#     json_file = open(json_file, "r")
#     run_information = json_file.read()
#     print(run_information)
#     run_information = json.loads(run_information)
#     #  print(run_information['run1']['binning'])
#
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
# print(files)
# #color_channel = run_information[run]['color_channel']
# #binning = run_information[run]['binning']
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
    print(run_information)
    run_information = json.loads(run_information)
    #  print(run_information['run1']['binning'])

    def inner_func():
        print(run_information)

    return "in admin fun"


@app.route("/adminPanel", methods=['POST'])
def test_timeit():
    setup = '''
from simulator import admin_fun
admin_fun()     
    '''
    timeit.timeit('inner_func()', setup=setup)

def save_results(results):
    fo = open("result.txt", "a")
    fo.write(results)
    fo.write("\n")
    # Close opend file
    fo.close()



    # timeit.timeit(get_files(file_path, frequency, binning,
    #                         color_channel, connect_kafka),
    #               '''from __main__ import get_files,'
    #                 'file_path, frequency=0, color_channel,'
    #                 'binning, connect_kafka''')
    # (stmt='pass', setup='pass', timer=<default timer>, number=1000000, globals=None)


def retrieval_time():
    #kolla hur lång tid varje steg i (inre) for-loopen tar för att hämta bilder
    #output: medelvärde, std, var, histogram över alla frekvenser
    #1. set freq = 0
    pass


if __name__ == "__main__":
    app.run(debug=True)
