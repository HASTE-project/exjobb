import os
import random
import threading
import time

import cv2
from flask import Flask, render_template, request
from kafka import SimpleProducer, KafkaClient
from kafka.common import LeaderNotAvailableError


def connect(message):
    kafka = KafkaClient("129.16.125.242:9092")
    producer = SimpleProducer(kafka)
    topic = 'test'
    msg = b'Hello from the other side!'

    try:
        print_response(producer.send_messages(topic, message))
    except LeaderNotAvailableError:
        # https://github.com/mumrah/kafka-python/issues/249
        time.sleep(1)
        print_response(producer.send_messages(topic, message))

    kafka.close()

    #add randomness in time in datageneration (maybe better with normal distribution??)
    interval = random.uniform(freq-freq/5, freq-freq/5)
    threading.Timer(interval,main,[freq]).start()


def get_files():
    kafka = KafkaClient("129.16.125.242:9092")
    producer = SimpleProducer(kafka)
    topic = 'test'

    for root, dirs, files in os.walk('/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/'):

        for i in range(len(files)):
            img = cv2.imread('/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell '
                             '24h_20151215_110422/AssayPlate_NUNC_#165305-1/' + files[i])
            ret, jpeg = cv2.imencode('.png', img)
            producer.send_messages(topic, jpeg.tobytes())
    kafka.close()



