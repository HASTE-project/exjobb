import os
import random
import threading
import time

import cv2
from flask import Flask, render_template, request
from kafka import SimpleProducer, KafkaClient
from kafka.common import LeaderNotAvailableError


def connect(message):
    kafka = KafkaClient("129.16.125.231:9092")
    producer = SimpleProducer(kafka)
    topic = 'test'

    try:
        producer.send_messages(topic, message)
    except LeaderNotAvailableError:
        # https://github.com/mumrah/kafka-python/issues/249
        time.sleep(1)
        print_response(producer.send_messages(topic, message))

    kafka.close()


def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))
