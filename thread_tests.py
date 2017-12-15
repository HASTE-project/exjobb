import threading
import time
import cv2
import numpy as np

from PIL import Image
from kafka import KafkaConsumer


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter, consumer):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.consumer = consumer

    def run(self):
        print("Starting " + self.name)
        print_time(1, self.counter)
        python_kafka_consumer_performance(self.consumer)
        print("Exiting " + self.name)


def print_time(delay, counter):
    while counter:
        time.sleep(delay)
        print("counter: {}".format(counter))
        counter -= 1


# Create new threads
thread1 = myThread(1, "Thread-1", 4, "consumer1")
thread2 = myThread(2, "Thread-2", 4, "consumer2")

thread1.start()
thread2.start()

#thread1.join()
#thread2.join()

msg_count = 50


def python_kafka_consumer_performance(consumer):
    topic = 'test5part'

    # consumer = KafkaConsumer(
    #     bootstrap_servers=["130.239.81.54:9092"],
    #     auto_offset_reset='earliest',  # start at earliest topic
    #     group_id=None  # do no offest commit
    # )

    consumer1 = KafkaConsumer(group_id='my-group',
                              auto_offset_reset='earliest',
                              bootstrap_servers=["130.239.81.54:9092"])
    # consumer2 = KafkaConsumer(group_id='my-group',
    #                           auto_offset_reset='earliest',
    #                           bootstrap_servers=["130.239.81.54:9092"])

    msg_consumed_count = 0


    consumer1.subscribe([topic])
    consumer_start = time.time()
    # consumer2.subscribe([topic])
    for message in consumer1:
        print("{}, msg nb: {}".format(consumer, msg_consumed_count))
        msg_consumed_count += 1
        img = cv2.imdecode(np.frombuffer(message.value, dtype=np.uint16), -1)
        fin2 = Image.fromarray(img)

        if msg_consumed_count >= msg_count/2:
            break

    consumer_timing = time.time() - consumer_start
    print("{} consumer_time: {}".format(consumer, consumer_timing))
    consumer1.close()
