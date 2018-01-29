import time

"""
Use like this to generate CSV output:
python3 example_simulator_no_flask_dummy_set.py | tee >(grep --line-buffered "^benchmarking," > benchmarking.csv)
"""


__printed_header = False

def start_benchmark():
    return time.time()


def end_benchmark(file, topic, started_at_time, description='', number_of_bytes=-1):
    global __printed_header
    ended_time = time.time()

    if not __printed_header:
        __printed_header = True
        print(','.join([
            'benchmarking',
            'file',
            'topic',
            'description',
            'started_at_time',
            'ended_time',
            'duration_secs',
            'number_of_bytes']))

    columns = ['benchmarking',
               file,
               topic,
               description,
               str(started_at_time),
               str(ended_time),
               str(ended_time - started_at_time),  # TODO: ensure sci-not can be parsed ?
               str(number_of_bytes)]

    row = ','.join(columns)
    print(row, flush=True)  # Flushing helps with docker containers


if __name__ == '__main__':
    start = start_benchmark()
    end_benchmark('foo_file','foo_topic', start, description='foo description', number_of_bytes=5)
