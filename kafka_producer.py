"""Module to connect to Kafka server and send messages to Kafka producer."""

import os
import random
import threading
import time

from kafka import SimpleProducer, KafkaClient
from kafka.common import LeaderNotAvailableError


# def connect():
#     kafka = KafkaClient("129.16.125.231:9092")
#     producer = SimpleProducer(kafka)
#     topic = 'test'
#     return [topic, producer]

def connect(message):
    kafka = KafkaClient("130.239.81.54:9092")
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
