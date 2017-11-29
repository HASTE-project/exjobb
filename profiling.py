# start a new test, run and save score
# use time.clock()
# test max freq - check how long time each iteration in the for-loop takes (ie. time to retrive each image)
# test if set freq corresponds to actual freq
# test freq for different image sizes
# maybe test if there are differences when storing images in a volume and in object store

# input: JSON file with test settings (possible to make multiple runs at once)
# output: 1. text file with freq info 2. graphs showing performance

import json
import os
import numpy as np
import time
import cv2
import csv
import kafka_producer
import sys

from kafka import SimpleProducer, KafkaClient
from kafka.common import LeaderNotAvailableError

from skimage.measure import block_reduce
from skimage import img_as_uint


def time_get_files(file_path, frequency, binning, color_channel, connect_kafka):
    result = []
    files = os.listdir(file_path)

    if frequency == 0:
        for file in files:
            start = time.clock()
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:
                    img = cv2.imread(file_path + file, -1)
                    #print(type(img))
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        kafka_producer.connect(jpeg.tobytes())
            stop = time.clock()
            result.append(stop-start)
    else:
        for file in files:
            start = time.clock()
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:
                    img = cv2.imread(file_path + file, -1)
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        kafka_producer.connect(jpeg.tobytes())
            time.sleep(frequency)
            stop = time.clock()
            result.append(stop-start)
    return result


def timer(file_path):
    json_file = open(file_path, "r")
    run_information = json_file.read()
    json_file.close()
    run_information = json.loads(run_information)

    for run in run_information:
        frequency = run_information[run]['frequency']
        color_channel = run_information[run]['color_channel']
        binning = run_information[run]['binning']
        file_path = run_information[run]['file_path']
        connect_kafka = run_information[run]['connect_kafka']
        result = time_get_files(file_path, frequency, binning, color_channel, connect_kafka)
        save_as_csv(result, run)


def timer_kafka(file_path, to_time):
    json_file = open(file_path, "r")
    run_information = json_file.read()
    json_file.close()
    run_information = json.loads(run_information)
    for run in run_information:
        frequency = run_information[run]['frequency']
        color_channel = run_information[run]['color_channel']
        binning = run_information[run]['binning']
        file_path = run_information[run]['file_path']
        connect_kafka = run_information[run]['connect_kafka']
        if to_time == "p":
            result = time_kafka_producer(file_path, frequency, binning, color_channel, connect_kafka)
        elif to_time == "p2":
            result = time_kafka_producer2(file_path, frequency, binning, color_channel, connect_kafka) 
        elif to_time == "c":
            result = time_kafka_consumer(file_path, frequency, binning, color_channel, connect_kafka)
        elif to_time == "g":
            result = time_get_files(file_path, frequency, binning, color_channel, connect_kafka)
        else:
            raise AssertionError("Specify what to time (p=producer, c=consumer, g=get_files)")
        save_as_csv(result, run)


def time_kafka_producer(file_path, frequency, binning, color_channel, connect_kafka):
    result = []
    files = os.listdir(file_path)
    if frequency == 0:
        for file in files:
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:
                    img = cv2.imread(file_path + file, -1)
                    #print(type(img))
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        as_bytes = jpeg.tobytes()
                        start = time.clock()
                        kafka_producer.connect(as_bytes)
                        stop = time.clock()
                        result.append(stop-start)
    else:
        for file in files:
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:
                    img = cv2.imread(file_path + file, -1)
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        as_bytes = jpeg.tobytes()
                        start = time.clock()
                        kafka_producer.connect(as_bytes)
                        time.sleep(frequency)
                        stop = time.clock()
                        result.append(stop-start)
    return result


def time_kafka_producer2(file_path, frequency, binning, color_channel, connect_kafka):
    kafka = KafkaClient("129.16.125.249:9092")
    producer = SimpleProducer(kafka)
    topic = 'test'
    result = []
    files = os.listdir(file_path)
    if frequency == 0:
        for file in files:
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:
                    img = cv2.imread(file_path + file, -1)
                    #print(type(img))
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        as_bytes = jpeg.tobytes()
                        #start = time.clock()
                        #kafka_producer.connect(as_bytes)
                        try:
                            start = time.clock()
                            producer.send_messages(topic, as_bytes)
                            stop = time.clock()
                            result.append(stop-start)
                        except LeaderNotAvailableError:
                            # https://github.com/mumrah/kafka-python/issues/249
                            time.sleep(1)
                            print_response(producer.send_messages(topic, as_bytes))
                        #stop = time.clock()
                        #result.append(stop-start)
    else:
        for file in files:
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:
                    img = cv2.imread(file_path + file, -1)
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        as_bytes = jpeg.tobytes()
                        #start = time.clock()
                       # kafka_producer.connect(as_bytes)
                        try:
                            start = time.clock()
                            producer.send_messages(topic, as_bytes)
                            time.sleep(frequency)
                            stop = time.clock()
                            result.append(stop-start)
                        except LeaderNotAvailableError:
                            # https://github.com/mumrah/kafka-python/issues/249
                            time.sleep(1)
                            print_response(producer.send_messages(topic, as_bytes))
                        #time.sleep(frequency)
                        #stop = time.clock()
                        #result.append(stop-start)
        kafka.close()
    return result


def timer_kafka_100bytes():
    kafka = KafkaClient("129.16.125.249:9092")
    producer = SimpleProducer(kafka)
    topic = 'test'
    result = []
    message = b"0" * 67 #overhead of 33 bytes 
    print(sys.getsizeof(message))
    for i in range(1000):
        try:
            start = time.clock()
            producer.send_messages(topic, message)
            stop = time.clock()
            result.append(stop - start)
        except LeaderNotAvailableError:
            # https://github.com/mumrah/kafka-python/issues/249
            time.sleep(1)
            print_response(producer.send_messages(topic, message))
    kafka.close()
    save_as_csv(result, "100bytes")



def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))


def time_kafka_consumer(file_path, frequency, binning, color_channel, connect_kafka):
    result = []
    files = os.listdir(file_path)

    consumer = KafkaConsumer(group_id=b"my_group_id",
                             bootstrap_servers=["129.16.125.231:9092"])  # ,

    consumer.subscribe(topics=['test'])

    def events():
        print("in events")
        for message in consumer:
            # print(message.value)
            ty = type(message.value)
            print(ty)
            # imgfile = BytesIO(message.value)
            # img = Image.open(imgfile)
            # img.save(os.path.join(os.path.expanduser('~'), str(message.offset) + ".tiff"))

            img = cv2.imdecode(np.frombuffer(message.value, dtype=np.uint16), -1)
            print("type img : {}".format(type(img)))
            print("size img: {}".format(img.shape))
            fin2 = Image.fromarray(img)
            print("fin2 type: {}".format(type(fin2)))
            fin2.save(str(message.offset) + ".tif")





    if frequency == 0:
        for file in files:
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:
                    img = cv2.imread(file_path + file, -1)
                    #print(type(img))
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        start = time.clock()
                        kafka_producer.connect(jpeg.tobytes())
                        stop = time.clock()
                        result.append(stop-start)
    else:
        for file in files:
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:
                    img = cv2.imread(file_path + file, -1)
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        start = time.clock()
                        kafka_producer.connect(jpeg.tobytes())
                        time.sleep(frequency)
                        stop = time.clock()
                        result.append(stop-start)
    return result





def save_as_csv(results, run):
    with open(run + "result.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(results)


