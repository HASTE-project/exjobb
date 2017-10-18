import time, threading, random
import os
import cv2

from skimage.measure import block_reduce
from os.path import join, getsize
from flask import Flask, Response, render_template, request

app = Flask(__name__)

@app.route("/index")
def index():
    return render_template('start_page.html')

@app.route("/index", methods=['POST'])
def index_post():
    frequency = request.form["interval"]
    binning = request.form["binning"]
    color_channel = request.form.getlist("color_channel")
    interval = float(frequency)
    print("binning: {} color_channel: {}".format(binning, color_channel))
    main(interval)
    return "You are now writing to test.txt every {} second.".format(frequency)

def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))


def main(freq):
    interval = random.uniform(freq-freq/5, freq-freq/5)
    threading.Timer(interval,main,[freq]).start()


@app.route("/fileWalk")
def file_walk():
    return render_template('file_walk_page.html')

@app.route("/fileWalk", methods=['POST'])
def file_walk_post():
    get_files()
    return "You are now streaming file names with Kafka"

def get_files():

    for root, dirs, files in os.walk('/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/'):
       print("Length of 'files': {}", len(files))
       if type(files) is list:
          print("files is list")
       else:
          print("files is something else")
       if not files:
          print("files is empty")
       else:
          print("In else")
          print("root: ", root)
          print("dirs: ", dirs)
          print("files[0]: ", files[0])
          if not dirs:
             print("dirs is empty")
          print('/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/' + files[0])
          for index in range(len(files)):
             img = cv2.imread('/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/' + files[index])
             ret, jpeg = cv2.imencode('.png', img)

if __name__ == "__main__":
     app.run(debug=True)



