from flask import Flask, Response
from kafka import KafkaConsumer

#app = Flask(__name__)

#@app.route("/")
def main():
    consumer = KafkaConsumer(group_id=b"my_group_id",
                             bootstrap_servers=["lovisa:9092"],
                             value_deserializer = lambda m: m.decode('ascii'))

    consumer.subscribe(topics=['test'])

    def events():
       for message in consumer:
 #         if message is not None:
  #            result='{} {} '.format(message.value, message.offset) #.append('hello') #str(message.value).decode('utf-8'))  # <--- here (str)
   #       yield result
          f = open("test.txt","a") #opens file with name of "test.txt"

          f.write("\n {} offset: {} ".format(message.value, message.offset))

          f.close()

         # print(message.value)
#    for message in consumer:
        # This will wait and print messages as they become available
       # print('Offset: %s' % message.offset)
 #       return 'Offset: %s' % message.offset
    return Response(events())

if __name__ == "__main__":
   # index()
    main()
 #  app.run(debug=True)

