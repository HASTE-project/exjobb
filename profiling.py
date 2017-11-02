import timeit
import json
import os

from flask import request


def admin_fun():
    #test max freq - kolla hur lång tid varje steg i for-loopen tar
    #test if set freq corresponds to actual freq
    #test freq for different image sizes

    # input: JSON file with test settings (possible to make multiple runs at once)
    json_file = request.form["file_path"]
    json_file = open(json_file, "r")
    run_information = json_file.read()
    print(run_information)
    run_information = json.loads(run_information)
    #  print(run_information['run1']['binning'])

    def inner_func():
        print(run_information)



    return ("in admin fun")

def test_timeit():
    setup = '''\
...from __main__ import admin_fun     
    '''
    timeit.timeit('inner_func()', setup=setup)

def save_results(results):
    fo = open("result.txt", "a")
    fo.write(results)
    fo.write("\n")
    # Close opend file
    fo.close()