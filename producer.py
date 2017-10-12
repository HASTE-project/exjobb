import time, threading, random
import os

from os.path import join, getsize
from kafka import SimpleProducer, KafkaClient
from kafka.common import LeaderNotAvailableError
from flask import Flask, Response, render_template, request

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
    kafka = KafkaClient("129.16.125.242:9092")
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
    kafka = KafkaClient("129.16.125.242:9092")
    producer = SimpleProducer(kafka)
    topic = 'test'

    for root, dirs, files in os.walk('/mnt/volume/fromAl/'):
       print("Length of 'files': {}", len(files))
       if type(files) is list:
          print("files is list")
       else:
          print("files is something else")
       if not files:
          print("files is empty")
       else:
          print("In else")
          for index in range(len(files)):
             msg = bytes(files[index], 'utf-8')
             producer.send_messages(topic, msg)
       kafka.close()

if __name__ == "__main__":
     app.run(debug=True)
