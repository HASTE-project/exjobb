import json
import timeit


def test_timeit(runs):

    setup_template = '''
from simulatorNoFlask import read_from_json, get_files
run_information = read_from_json('test.json') 
frequency = run_information['run']['frequency']
color_channel = run_information['run']['color_channel']
binning = run_information['run']['binning']
file_path = run_information['run']['file_path']
connect_kafka = run_information['run']['connect_kafka']   
    '''

    for run in range(runs):
        setup = setup_template.replace("'run'", "'run{}'".format(run))
        save_results(str(timeit.timeit('get_files(file_path, frequency, binning, color_channel, connect_kafka)',
                                       setup=setup, number=3)), run)

    return "test ready"

def read_from_json(json_file):
    json_file = open(json_file, "r")
    run_information = json_file.read()
    json_file.close()
    run_information = json.loads(run_information)
    return run_information
