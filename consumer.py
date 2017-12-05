import cv2
import os
import numpy as np

from PIL import Image
from io import StringIO, BytesIO
from flask import Flask, Response
from kafka import KafkaConsumer


def main():
    consumer = KafkaConsumer(group_id=b"my_group_id",
                             bootstrap_servers=["130.239.81.54:9092"]) #,

    consumer.subscribe(topics=['test'])



    def events():
        print("in events")
        for message in consumer:
            #print(message.value)
            ty = type(message.value)
            print(ty)
            # imgfile = BytesIO(message.value)
            # img = Image.open(imgfile)
            # img.save(os.path.join(os.path.expanduser('~'), str(message.offset) + ".tiff"))

             img = cv2.imdecode(np.frombuffer(message.value, dtype=np.uint16), -1)
             print("type img : {}".format(type(img)))
             print("size img: {}".format(img.shape))
             fin2 = Image.fromarray(img)
             print("fin2 type: {}".format(type(fin2)))
             fin2.save(str(message.offset) + ".tif")

            # with open(os.path.join(os.path.expanduser('~'), str(message.offset) + ".bin"), 'wb+') as f:
            #     f.write(b'Content-Type: image/png\r\n\r\n' + message.value + b'\r\n\r\n')

            # cv2.imwrite(os.path.join(os.path.expanduser('~'), str(message.offset) + ".png"), imag)

            print("efter imwrite")
            #      f = open("test.txt","a") #opens file with name of "test.txt"
            #     f.write("\n offset: {} ".format(message.offset))

            #    f.close()

            # print(message.value)
            #    for message in consumer:
            # This will wait and print messages as they become available
            # print('Offset: %s' % message.offset)
            #       return 'Offset: %s' % message.offset
    return Response(events())

if __name__ == "__main__":
    # index()
    main()
#    app.run(debug=True)

