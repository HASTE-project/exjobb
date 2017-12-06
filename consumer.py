import cv2
import numpy as np

from PIL import Image
from flask import Response
from kafka import KafkaConsumer


def main():
    consumer = KafkaConsumer(group_id=b"my_group_id",
                             bootstrap_servers=["130.239.81.54:9092"])

    consumer.subscribe(topics=['test'])

    def events():
        print("in events")
        for message in consumer:
            ty = type(message.value)
            print(ty)
            print("message.key: {}".format(message.key.decode("utf-8")))
      #      img = cv2.imdecode(np.frombuffer(message.value, dtype=np.uint16), -1)
     #       print("type img : {}".format(type(img)))
    #        print("size img: {}".format(img.shape))
   #         fin2 = Image.fromarray(img)
  #          print("fin2 type: {}".format(type(fin2)))
 #           fin2.save(messafe.key.decode("utf-8") + ".tif")

    return Response(events())


if __name__ == "__main__":
    main()
