import cv2
import os
import numpy as np

from PIL import Image
from io import StringIO, BytesIO
from flask import Flask, Response
from kafka import KafkaConsumer

#app = Flask(__name__)

#@app.route("/")

#consumer = KafkaConsumer(group_id=b"my_group_id",
 #                        bootstrap_servers=["129.16.125.242:9092"]) #,
#                         value_deserializer = lambda m: m.decode('ascii'))

#consumer.subscribe(topics=['test'])


def main():
    consumer = KafkaConsumer(group_id=b"my_group_id",
                             bootstrap_servers=["129.16.125.231:9092"]) #,
#                             value_deserializer = lambda m: m.decode('ascii'))

    consumer.subscribe(topics=['test'])

   # return Response(events(),
    #                mimetype='multipart/x-mixed-replace; boundary=frame')



    def events():
        print("in events")
        for message in consumer:
 #         if message is not None:
  #            result='{} {} '.format(message.value, message.offset) #.append('hello') #str(message.value).decode('utf-8'))  # <--- here (str)
   #       yield result
           print(message.offset)
#           yield (b'--frame\r\n'
 #                 b'Content-Type:image/png\r\n\r\n' + message.value + b'\r\n\r\r')
           #safe image as png
           imgfile = BytesIO(message.value)
           img = Image.open(imgfile)
           img.save(os.path.join(os.path.expanduser('~'), str(message.offset) + ".png"))

#           imag = np.fromstring(message.value, sep ="/")
 #          print("imag: {}".format(imag))
  #         print("type(imag): {}".format(type(imag)))
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

