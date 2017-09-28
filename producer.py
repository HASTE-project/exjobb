import time, threading, random

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
    kafka = KafkaClient("lovisa:9092")
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

if __name__ == "__main__":
     app.run(debug=True)
