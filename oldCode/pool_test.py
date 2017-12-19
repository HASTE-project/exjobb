import time
from multiprocessing import Pool

import cv2
import numpy as np
from PIL import Image
from kafka import KafkaConsumer


def python_kafka_consumer_performance(consumer_number):
    topic = 'test5part'
    msg_count = 0
    print("in multip!")
    consumer = KafkaConsumer(group_id='my-group',
                             auto_offset_reset='earliest',
                             bootstrap_servers=["130.239.81.54:9092"])

    msg_consumed_count = 0
    print("msg_count: {}".format(msg_count))
    consumer.subscribe([topic])
    consumer_start = time.time()
    time.sleep(10)
    for message in consumer:
        print("{}, msg nb: {}".format(consumer_number, msg_consumed_count))
        msg_consumed_count += 1
        # img = cv2.imdecode(np.frombuffer(message.value, dtype=np.uint16), -1)
        # fin2 = Image.fromarray(img)
        if msg_consumed_count >= msg_count:
            break

    consumer_timing = time.time() - consumer_start
    print("{} consumer_time: {}".format(consumer_number, consumer_timing))
    consumer.close()
    return "done!"


agents = 2
if __name__ == '__main__':
    with Pool(processes=agents) as pool:
        # print("hoho")
        t = time.clock()
        print(pool.apply_async(python_kafka_consumer_performance, ['1']).get())
        print(pool.apply_async(python_kafka_consumer_performance, ['2']).get())

      #  [pool.apply_async(python_kafka_consumer_performance, t).get() for t in ['3', '4']]
        print("total time: {}".format(time.clock()-t))

print("done with pool")


# def f(x):
#     print("hej")
#     return x * x
#
#
# if __name__ == '__main__':
#     with Pool(5) as p:
#         print(p.map(f, [1, 2, 3]))
