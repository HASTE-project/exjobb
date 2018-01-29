import run_prod_pipeline_from_volume
import run_prod_pipeline_dummy_set
import benchmarking
import time
from pymongo import MongoClient

"""
python3 benchmark_full_pipeline.py | tee >(grep --line-buffered "^benchmarking," > benchmarking.csv)
"""


# TODO: this should be in its own repo, with the simulator as a dependency.

def wait_for_record_count(py_collection, target_count):
    started = time.time()
    while time.time() < started + (60 * 60):
        print('polling...', flush=True)
        count_now = py_collection.find().count()
        print('count is: ' + str(count_now))

        remaining = target_count - count_now
        if remaining <= 0:
            return
        if remaining > 100:
            time.sleep(1)
        elif remaining > 10:
            time.sleep(.1)
        else:
            time.sleep(.01)


benchmarking.enable()

benchmark_full_pipeline_start = benchmarking.start_benchmark()

stream_id = str(run_prod_pipeline_from_volume.run())
#stream_id = str(run_prod_pipeline_dummy_set.run())

print('Stream ID is:' + stream_id)

# Poll the database to check for completion
mongo_client = MongoClient('mongodb://192.168.1.7:27017')
#mongo_client = MongoClient('mongodb://metadata-db-prod:27017')

mongo_db = mongo_client.streams

# The name of the MongoDB collection is the stream ID:
collection = mongo_db[stream_id]

wait_for_record_count(collection, target_count=500)

benchmarking.end_benchmark('benchmark_full_pipeline', 'full', benchmark_full_pipeline_start)

