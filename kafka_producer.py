"""Module to connect to Kafka server and send messages to Kafka producer."""

import time

from kafka import KafkaProducer, KafkaClient, SimpleProducer
from kafka.common import LeaderNotAvailableError


def connect():
    # kafka = KafkaClient("129.16.125.231:9092")
    producer = KafkaProducer(bootstrap_servers=["130.239.81.54:9092"])
    topic = 'test'
    print(type(producer))
    return [topic, producer]


def old_connect(message):
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


def send_kafka_message(producer, topic, message, file_name):
    # kafka = KafkaClient("130.239.81.54:9092")
    # producer = SimpleProducer(kafka)
    topic = 'test'
#    producer = KafkaProducer(bootstrap_servers=["130.239.81.54:9092"])
    producer = KafkaProducer(bootstrap_servers=["130.239.81.54:9092"])
    print("in send_msg!")
    print("prod: {} topic: {}".format(producer, topic))

    try:
        producer.send(topic, key=str.encode(file_name), value=message)
      #  producer.send(topic, key=file_name, value=message)
        print("msg sent!")
    except LeaderNotAvailableError:
        print("in except :(")
        # https://github.com/mumrah/kafka-python/issues/249
        time.sleep(1)
        print_response(producer.send(topic, key=file_name, value=message))


#  kafka.close()


def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))
