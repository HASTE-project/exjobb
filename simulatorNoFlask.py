import time, random
import numpy as np
import os
import cv2
import timeit
import json
import kafka_producer

from skimage import img_as_ubyte
from skimage.measure import block_reduce


def hoho(st):
    print(st)


def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))


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


def time_get_files(file_path, frequency, binning, color_channel, connect_kafka):
    result = []
    for root, dirs, files in os.walk(file_path):
        if not files:
            pass
        else:
            if not dirs:
                pass
            if frequency == 0:
                for i in range(len(files)):
                    start = time.clock()
                    if files[i][-5] in color_channel:
                        img = cv2.imread(file_path + files[i], -1)
                        binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                        if connect_kafka == "yes":
                            ret, jpeg = cv2.imencode('.png', img_as_ubyte(binned_img))
                            kafka_producer.connect(jpeg.tobytes())
                    stop = time.clock()
                    result.append(stop-start)
            else:
                for i in range(len(files)):
                    start = time.clock()
                    if files[i][-5] in color_channel:
                        img = cv2.imread(file_path + files[i], -1)
                        binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                        if connect_kafka == "yes":
                            ret, jpeg = cv2.imencode('.png', img_as_ubyte(binned_img))
                            kafka_producer.connect(jpeg.tobytes())
                    time.sleep(frequency)
                    stop = time.clock()
                    result.append(stop-start)
            print(result)
    return result


# start a new test run and save score
# use timeit
# files = os.listdir(file_path)
# output: 1. text file with freq info 2. graphs showing performance

def admin_fun(json_file):
    #test max freq - kolla hur lång tid varje steg i for-loopen tar
    #test if set freq corresponds to actual freq
    #test freq for different image sizes

    # input: JSON file with test settings (possible to make multiple runs at once)
    json_file = open(json_file, "r")
    run_information = json_file.read()
    json_file.close()
    run_information = json.loads(run_information)
    return run_information


def test_timeit(runs):

    setup_template = '''
from simulatorNoFlask import admin_fun, get_files
run_information = admin_fun('test.json') 
frequency = run_information['run']['frequency']
color_channel = run_information['run']['color_channel']
binning = run_information['run']['binning']
file_path = run_information['run']['file_path']
connect_kafka = run_information['run']['connect_kafka']   
    '''

    for run in range(runs):
        setup = setup_template.replace("'run'", "'run{}'".format(run))
        save_results(str(timeit.timeit('get_files(file_path, frequency, binning, color_channel, connect_kafka)',
                                       setup=setup, number=3)), run)

    return "test ready"


def timer(file_path):
    run_information = admin_fun(file_path)
    print(len(run_information))
    for run in run_information:
        frequency = run_information[run]['frequency']
        color_channel = run_information[run]['color_channel']
        binning = run_information[run]['binning']
        file_path = run_information[run]['file_path']
        connect_kafka = run_information[run]['connect_kafka']
        create_hist(time_get_files(file_path, frequency, binning, color_channel, connect_kafka))


def save_results(results, run):
    fo = open("result.txt", "a")
    fo.write("Run nr, result: {} ".format(run))
    fo.write(results)
    fo.write("\n")
    fo.close()


def create_hist(data):
    np.histogram(data)
