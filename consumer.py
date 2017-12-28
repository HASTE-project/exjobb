import cv2
import numpy as np

from PIL import Image
from flask import Response
from kafka import KafkaConsumer
from myvariables import kafka_server, topic


def main():
    consumer = KafkaConsumer(group_id=b"my_group_id",
                             bootstrap_servers=[kafka_server + ":9092"],
                             max_partition_fetch_bytes=10000000)

    consumer.subscribe(topics=[topic])

    def events():
        print("in events")
        for message in consumer:
            # ty = type(message.value)
            print(message.offset)
            # print("message.key: {}".format(message.key.decode("utf-8")))
            img = cv2.imdecode(np.frombuffer(message.value, dtype=np.uint16), -1)
            # print("type img : {}".format(type(img)))
            # print("size img: {}".format(img.shape))
            fin2 = Image.fromarray(img)
            # print("fin2 type: {}".format(type(fin2)))
            fin2.save(message.key.decode("utf-8"))

    return Response(events())


if __name__ == "__main__":
    main()
