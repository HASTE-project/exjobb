t1 = time.clock()
p1 = multiprocessing.Process(target=pkcp.python_kafka_consumer_performance, args="1")

p2 = multiprocessing.Process(target=pkcp.python_kafka_consumer_performance, args="2")

#   p3 = multiprocessing.Process(target=python_kafka_consumer_performance, args="3")
#   p4 = multiprocessing.Process(target=python_kafka_consumer_performance, args="4")
#   p5 = multiprocessing.Process(target=python_kafka_consumer_performance, args="5")

p1.start()
p2.start()
#  p3.start()
#  p4.start()
# p5.start()

p1.join()
p2.join()
print("time: {}".format(time.clock() - t1))
#  p3.join()
#  p4.join()
#  p5.join()

print("Done!")
