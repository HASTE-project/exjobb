import os
import random
import threading
import time

import cv2
from flask import Flask, render_template, request
from kafka import SimpleProducer, KafkaClient
from kafka.common import LeaderNotAvailableError

app = Flask(__name__)


@app.route("/index")
def index():
    return render_template('start_page.html')


@app.route("/index", methods=['POST'])
def index_post():
    frequency = request.form["interval"]
    interval = float(frequency)
    main(interval)
    return "You are now writing to test.txt every {} second.".format(frequency)


def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))


def main(freq):
    kafka = KafkaClient("129.16.125.231:9092")
    producer = SimpleProducer(kafka)

    topic = 'test'
    msg = b'Hello from the other side!'

    try:
        print_response(producer.send_messages(topic, msg))
    except LeaderNotAvailableError:
        # https://github.com/mumrah/kafka-python/issues/249
        time.sleep(1)
        print_response(producer.send_messages(topic, msg))

    kafka.close()

    #add randomness in time in datageneration (maybe better with normal distribution??)
    interval = random.uniform(freq-freq/5, freq-freq/5)
    threading.Timer(interval,main,[freq]).start()


@app.route("/fileWalk")
def file_walk():
    return render_template('file_walk_page.html')


@app.route("/fileWalk", methods=['POST'])
def file_walk_post():
    get_files()
    return "You are now streaming file names with Kafka"


def get_files():
    kafka = KafkaClient("129.16.125.231:9092")
    producer = SimpleProducer(kafka)
    topic = 'test'

    for root, dirs, files in os.walk('/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/'):
        if not files:
            print("files is empty")
        else:
            print("In else")
            print("root: ", root)
            print("dirs: ", dirs)
            print("files[0]: ", files[0])
            if not dirs:
                print("dirs is empty")
            #          else:
            print('/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell '
                  '24h_20151215_110422/AssayPlate_NUNC_#165305-1/' + files[0])
            for i in range(len(files)):
                img = cv2.imread('/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell '
                                 '24h_20151215_110422/AssayPlate_NUNC_#165305-1/' + files[i])
                ret, jpeg = cv2.imencode('.png', img)
                producer.send_messages(topic, jpeg.tobytes())
        kafka.close()


if __name__ == "__main__":
    app.run(debug=True)
