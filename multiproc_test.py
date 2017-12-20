#GO for this!!! (not threading or pool)

import multiprocessing
import time

import python_kafka_consumer_perf as pkcp



def start_processes(num_of_proc):

    file = open("consumer_res.txt", "a")
    all_processes = []
    t = time.time()
    file.write("\n{}".format(time.time()))
    for i in range(num_of_proc):
       # print(i)
        all_processes.append(multiprocessing.Process(target=pkcp.python_kafka_consumer_performance, args=str(i)))

    for i in range(num_of_proc):
        all_processes[i].start()

    for i in range(num_of_proc):
        all_processes[i].join()
        print("time: {}".format(time.clock() - t))


if __name__ == "__main__":

    ta = time.time()
    start_processes(1)
    print("own impl time: {}".format(time.time()-ta))


