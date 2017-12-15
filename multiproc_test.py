import multiprocessing
import time

from kafka import KafkaConsumer


def python_kafka_consumer_performance(consumer_number):
    topic = 'test5part'
    msg_count = 50

    consumer = KafkaConsumer(group_id='my-group',
                             auto_offset_reset='earliest',
                             bootstrap_servers=["130.239.81.54:9092"])

    msg_consumed_count = 0

    consumer.subscribe([topic])
    consumer_start = time.time()
    for message in consumer:
        #print("{}, msg nb: {}".format(consumer_number, msg_consumed_count))
        msg_consumed_count += 1
        img = cv2.imdecode(np.frombuffer(message.value, dtype=np.uint16), -1)
        fin2 = Image.fromarray(img)
        if msg_consumed_count >= msg_count / 5:
            break

    consumer_timing = time.time() - consumer_start
    print("{} consumer_time: {}".format(consumer_number, consumer_timing))
    consumer.close()













if __name__ == "__main__":
    p1 = multiprocessing.Process(target=python_kafka_consumer_performance, args="1")
    p2 = multiprocessing.Process(target=python_kafka_consumer_performance, args="2")
    p3 = multiprocessing.Process(target=python_kafka_consumer_performance, args="3")
    p4 = multiprocessing.Process(target=python_kafka_consumer_performance, args="4")
    p5 = multiprocessing.Process(target=python_kafka_consumer_performance, args="5")

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()

    print("Done!")
