"""
This module profiles the simulator, Kafka producer and Kafka consumer with focus on throughput.
# start a new test, run and save score
# use time.clock()
# test max freq - check how long time each iteration in the for-loop takes (ie. time to retrieve each image)
# test if set freq corresponds to actual freq
# test freq for different image sizes

# input: JSON file with test settings (possible to make multiple runs at once)
# output: 1. csv file with freq info
 """

import csv
import json
import os
import time

import cv2
import numpy as np
from PIL import Image
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.common import LeaderNotAvailableError
from skimage import img_as_uint
from skimage.measure import block_reduce

import kafka_producer


def timer_kafka(file_path, to_time):
    """
    Function to time the simulator or the Kafka producer. The results are saved in a csv file named as the
    run. The inputs are given as a json-file where multiple runs with different settings can be defined at once.
    The to_time variable describes which function to time, it can be set to "p" (time Kafka producer),
    "p2" (time Kafka producer and start the Kafka connection beforehand) and "g" (time the simulator without
    Kafka).

    example:
    profiling.timer_kafka("test.json", "p")

    example test.json:
    {"run0": {"file_path": "path_to_image_files", "binning": 1,
    "period": 0.1, "color_channel": ["1","2", "3", "4", "5"], "connect_kafka": "No"}, "run1": {"file_path":
    "path_to_image_files", "binning": 2, "period": 2,
    "color_channel": ["1","2", "3", "4", "5"], "connect_kafka": "No"}}
    """

    json_file = open(file_path, "r")
    run_information = json_file.read()
    json_file.close()
    run_information = json.loads(run_information)
    for run in run_information:
        period = run_information[run]['period']
        color_channel = run_information[run]['color_channel']
        binning = run_information[run]['binning']
        file_path = run_information[run]['file_path']
        connect_kafka = run_information[run]['connect_kafka']
        if to_time == "p":
            result = time_kafka_producer(file_path, period, binning, color_channel, connect_kafka)
        elif to_time == "p2":
            result = time_kafka_producer2(file_path, period, binning, color_channel, connect_kafka)
        elif to_time == "g":
            result = time_get_files(file_path, period, binning, color_channel, connect_kafka)
        else:
            raise AssertionError("Specify what to time (p=producer, p2=producer (already connected to Kafka)"
                                 " , g=get_files)")
        save_as_csv(result, run)


def time_get_files(file_path, period, binning, color_channel, connect_kafka):
    result = []
    files = os.listdir(file_path)

    if period == 0:
        for file in files:
            start = time.clock()
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:  # 5th letter from the end of file name gives the color channel
                    img = cv2.imread(file_path + file, -1)
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        kafka_producer.connect(jpeg.tobytes())
            stop = time.clock()
            result.append(stop - start)
    else:
        print("period!=0")
        for file in files:
            start = time.perf_counter()
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:  # 5th letter from the end of file name gives the color channel
                    img = cv2.imread(file_path + file, -1)
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        kafka_producer.connect(jpeg.tobytes())
            time.sleep(period)
            stop = time.perf_counter()
            result.append(stop - start)
    return result


def time_kafka_producer(file_path, period, binning, color_channel, connect_kafka):
    result = []
    files = os.listdir(file_path)
    if period == 0:  # Stream as fast as possible.
        for file in files:
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:  # 5th letter from the end of file name gives the color channel
                    img = cv2.imread(file_path + file, -1)
                    # print(type(img))
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        as_bytes = jpeg.tobytes()
                        start = time.clock()
                        kafka_producer.old_connect(as_bytes)
                        stop = time.clock()
                        result.append(stop - start)
    else:  # Stream with given time period.
        for file in files:
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:  # 5th letter from the end of file name gives the color channel
                    img = cv2.imread(file_path + file, -1)
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        as_bytes = jpeg.tobytes()
                        start = time.clock()
                        kafka_producer.old_connect(as_bytes)
                        time.sleep(period)
                        stop = time.clock()
                        result.append(stop - start)
    return result


def time_kafka_producer2(file_path, period, binning, color_channel, connect_kafka):
    #   kafka = KafkaClient("130.239.81.54:9092")
    # producer = SimpleProducer(kafka)
    producer = KafkaProducer(bootstrap_servers=["130.239.81.54:9092"])
    # producer = KafkaProducer(bootstrap_servers=['broker1:1234'])
    topic = 'test'
    result = []
    files = os.listdir(file_path)
    if period == 0:  # Stream as fast as possible.
        for file in files:
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:  # 5th letter from the end of file name gives the color channel
                    img = cv2.imread(file_path + file, -1)
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        as_bytes = jpeg.tobytes()
                        try:
                            start = time.clock()
                            producer.send(topic, key=str.encode(file), value=as_bytes)
                            stop = time.clock()
                            result.append(stop - start)
                        except LeaderNotAvailableError:
                            # https://github.com/mumrah/kafka-python/issues/249
                            time.sleep(1)
                            producer.send(topic, key=str.encode(file), value=as_bytes)
                            # print_response(producer.send_messages(topic, as_bytes))
    else:  # Stream with a given time period.
        for file in files:
            if os.path.isfile(file_path + file):
                if file[-5] in color_channel:  # 5th letter from the end of file name gives the color channel
                    img = cv2.imread(file_path + file, -1)
                    binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
                    if connect_kafka == "yes":
                        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
                        as_bytes = jpeg.tobytes()
                        try:
                            start = time.clock()
                            #                            producer.send_messages(topic, as_bytes)
                            producer.send(topic, key=str.encode(file), value=as_bytes)
                            time.sleep(period)
                            stop = time.clock()
                            result.append(stop - start)
                        except LeaderNotAvailableError:
                            # https://github.com/mumrah/kafka-python/issues/249
                            time.sleep(1)
                            print_response(producer.send(topic, key=str.encode(file), value=as_bytes))
                        # print_response(producer.send_messages(topic, as_bytes))
    #   kafka.close()
    return result


def timer_kafka_100bytes():
    """Function which tests how fast writing to a Kafka topic is when the message is 100 bytes."""
    # kafka = KafkaClient("130.239.81.54:9092")
    #  producer = SimpleProducer(kafka)
    producer = KafkaProducer(bootstrap_servers=["130.239.81.54:9092"])
    topic = 'test'
    result = []
    message = b"0" * 67  # overhead of 33 bytes
    for i in range(1000):
        try:
            start = time.perf_counter()
            producer.send(topic, key=b'100bytes', value=message)
            # producer.send_messages(topic, message)
            stop = time.perf_counter()
            result.append(stop - start)
        except LeaderNotAvailableError:
            # https://github.com/mumrah/kafka-python/issues/249
            time.sleep(1)
            producer.send(topic, key=b'100bytes', value=message)
            # print_response(producer.send_messages(topic, message))
    # kafka.close()
    save_as_csv(result, "100bytes")


def time_kafka_consumer():
    """Function to time how Kafka consumer and conversion from bytes to tif. The results are saved in a csv file
    named consumer_test_result."""
    result = []

    consumer = KafkaConsumer(group_id=b"my_group_id",
                             bootstrap_servers=["130.239.81.54:9092"])

    consumer.subscribe(topics=['test'])

    for message in consumer:
        start = time.clock()
        img = cv2.imdecode(np.frombuffer(message.value, dtype=np.uint16), -1)
        fin2 = Image.fromarray(img)
        stop = time.clock()
        result.append(stop - start)
        fin2.save(str(message.offset) + ".tif")
        if os.path.isfile("consumer_test_result.csv"):
            with open("consumer_test_result.csv", "a") as f:
                wr = csv.writer(f)
                wr.writerow([stop - start])
        else:
            with open("consumer_test_result.csv", "a") as f:
                wr = csv.writer(f)
                wr.writerow([stop - start])

    return result


def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))


def save_as_csv(results, run):
    with open(run + "result.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(results)
