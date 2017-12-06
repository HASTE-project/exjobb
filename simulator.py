"""This module gives the simulator an interface. By starting simulator.py a Flask app is started and from the
web UI the user can change settings for the microscope simulator. The result is the same as starting
simulatorNoFlask.get_file(*args*)."""

from flask import Flask, render_template, request

# import kafka_producer
#import simulatorNoFlask

app = Flask(__name__)


def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))


@app.route("/fileWalk")
def file_walk():
    return render_template('file_walk_page.html')


@app.route("/fileWalk", methods=['POST'])
def file_walk_post():
    file_path = request.form["file_path"]
    print(file_path)
    period = request.form["period"]
    print(period)
    binning = int(request.form["binning"])
    print(binning)
    color_channel = request.form.getlist("color_channel")
    print(color_channel)
    connect_kafka = request.form["kafka"]
    print(connect_kafka)
    period = float(period)
   # simulatorNoFlask.get_files(file_path, period, binning, color_channel, connect_kafka)
    return "You are now streaming file names with Kafka"


# def get_files(file_path, period, binning, color_channel, connect_kafka):
#     print('in get_files')
#     for root, dirs, files in os.walk(file_path):
#         print('in for')
#         if not files:
#             print('in if')
#         #           pass
#         else:
#             if not dirs:
#                 print('if not dirs')
#             #		pass
#             for i in range(len(files)):
#                 #		print('2 for loop')
#
#                 simulatorNoFlask.get_file(files, color_channel, file_path, binning, connect_kafka)
#
#                 get_file(files, i, color_channel, file_path, binning, connect_kafka)
#                 #                simulatorNoFlask.get_file(files, color_channel, file_path, binning, connect_kafka)
#
#                 time.sleep(period)
#
#
# def get_file(files, i, color_channel, file_path, binning, connect_kafka):
#     print('in get_file')
#     if files[i][-5] in color_channel:
#         print('in color_channel')
#         img = cv2.imread(file_path + files[i], -1)
#         binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
#         if connect_kafka == "yes":
#             print('in connect_kafka')
#             ret, jpeg = cv2.imencode('.png', img_as_ubyte(binned_img))
#             kafka_producer.connect(jpeg.tobytes())


# def time_get_files(file_path, period, binning, color_channel, connect_kafka):
#     result = []
#     for root, dirs, files in os.walk(file_path):
#         if not files:
#             pass
#         else:
#             if not dirs:
#                 pass
#             if period == 0:
#                 for i in range(len(files)):
#                     start = time.clock()
#                     if files[i][-5] in color_channel:
#                         img = cv2.imread(file_path + files[i], -1)
#                         binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
#                         if connect_kafka == "yes":
#                             ret, jpeg = cv2.imencode('.png', img_as_ubyte(binned_img))
#                             kafka_producer.connect(jpeg.tobytes())
#                     stop = time.clock()
#                     result.append(stop - start)
#             else:
#                 for i in range(len(files)):
#                     start = time.clock()
#                     if files[i][-5] in color_channel:
#                         img = cv2.imread(file_path + files[i], -1)
#                         binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
#                         if connect_kafka == "yes":
#                             ret, jpeg = cv2.imencode('.png', img_as_ubyte(binned_img))
#                             kafka_producer.connect(jpeg.tobytes())
#                     time.sleep(period)
#                     stop = time.clock()
#                     result.append(stop - start)
#             print(result)


if __name__ == "__main__":
    app.run(debug=True)
