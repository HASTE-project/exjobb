import simulator_no_flask
import benchmarking
import time
from pymongo import MongoClient

"""
python3 benchmark_full_pipeline.py | tee >(grep --line-buffered "^benchmarking," > benchmarking.csv)
"""


# TODO: this should be in its own repo, with the simulator as a dependency.

def wait_for_record_count(py_collection, target_count):
    started = time.time()
    while time.time() < started + (60 * 60): # wait max of 1 hour for completion.
        print('polling...', flush=True)
        count_now = py_collection.find().count()
        print('count is: ' + str(count_now))
        remaining = target_count - count_now

        if count_now == 0 and time.time() > started + 60:
            print('timed out waiting for first item')
            return

        if remaining <= 0:
            return
        if remaining > 100:
            time.sleep(1)
        elif remaining > 10:
            time.sleep(.1)
        else:
            time.sleep(.01)

    print('timed out waiting for completion')


ip = '192.168.1.24'
dir = '/mnt/ImageData/testDatasets/0'

hio_config_ben_test_hio_example = {'master_host': ip,
                                   'master_port': 8080,
                                   'container_name': 'benblamey/hio-example:latest',
                                   'container_os': 'ubuntu'}

hio_config_ben_test_haste_example = {'master_host': ip,
                                     'master_port': 8080,
                                     'container_name': 'benblamey/haste-example:latest',
                                     'container_os': 'ubuntu'}

hio_config_hokan = {'master_host': '130.239.81.126',
                    'master_port': 8080,
                    'container_name': 'hakanwie/test:batch_hist2',
                    'container_os': 'ubuntu'}

hio_config_hw_image_proc = {'master_host': ip,
                            'master_port': 8080,
                            'container_name': 'benblamey/haste-image-proc:latest',
                            'container_os': 'ubuntu'}

hio_config_hw_image_proc_profiling = {'master_host': ip,
                                      'master_port': 8080,
                                      'container_name': 'benblamey/haste-image-proc:latest-profiling',
                                      'container_os': 'ubuntu'}

benchmarking.enable()

benchmark_full_pipeline_start = benchmarking.start_benchmark()

# get_files(file_path, period, binning, color_channel, send_to_target):
stream_id = simulator_no_flask.get_files(dir, 0, None, None, "yes",
                                         hio_config=hio_config_hw_image_proc,
                                         stream_id_tag='test_dataset_0')


# Poll the database to check for completion
mongo_client = MongoClient('mongodb://192.168.1.7:27017')
#mongo_client = MongoClient('mongodb://metadata-db-prod:27017')

mongo_db = mongo_client.streams

# The name of the MongoDB collection is the stream ID:
collection = mongo_db['strm_' + stream_id]

wait_for_record_count(collection, target_count=500)

benchmarking.end_benchmark('benchmark_full_pipeline', 'full', benchmark_full_pipeline_start)

