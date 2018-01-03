"""
Simulator program to simulate a microscope by setting frequency, binning and color channel. The simulator
can be attached to a streaming framework, at the moment Apache Kafka.

The simulator is started by calling:
simulatorNoFlask.get_files(file_path, frequency, binning, color_channel, connect_kafka)
file_path: where the image files are stored period: the period time between each image. The maximum
speed allowed by the system is retrieved when setting period to 0. binning: change image's binning to decrease
message size color_channel: set which color_channels to include, there are up to five channels (1-5), they are set by
giving a list, for example ['1','3'] sets color_channels 1 and 3.
connect_kafka: set to "yes" is Kafka is used as a streaming framework.
"""

import datetime
import os
import time

import cv2
import numpy as np
from skimage import img_as_uint
from skimage.measure import block_reduce

from hio_stream_target import HarmonicIOStreamTarget


def get_files(directory_path, period, binning, color_channel, send_to_target, hio_config=None, stream_id_tag='ll'):
    """
    This function retrieves files and creates a stream of files to be used as a microscope simulator.
    :param directory_path: path to directory containing image test data set files
    :param period: The time period between every image (setting to 0 gives minimal time period)
    :param binning: specify the binning (reduce the number of pixels to compress the image), this is given as an
    int. Or 'None' to use the original image.
    :param color_channel: filter files according to color channels to send (according to AZ convention), the channels
    are given as a list eg. ['1', '2'] (the Yokogawa microscope can have up to five color channels).
    Or 'None' to include all files.
    :param send_to_target: specify if the simulator shall stream images somewhere else with streaming framework
    :param hio_config: configuration dict for HarmonicIO integration. (see: hio_stream_target.py)
    :param stream_id_tag: string to use in stream ID
    """
    files = os.listdir(directory_path)
    print("simulator: list of files to stream:")
    print(files)
    stream_target = None

    stream_id = datetime.datetime.today().strftime('%Y_%m_%d__%H_%M_%S') + '_' + stream_id_tag
    print("simulator: stream ID is: " + stream_id)

    if send_to_target == "yes":
        # connect to stream target:
        # stream_target = KafkaStreamTarget() # TODO - pick one here. (or pass it in).
        stream_target = HarmonicIOStreamTarget(hio_config)
        # print(stream_target)
        # topic = stream_target[0]
        # producer = stream_target[1]
        print("simulator: initialized streaming target")
    else:
        print("simulator: skipping stream target initialization")
    # producer = None
    # topic = None

    for filename in files:
        full_path = os.path.join(directory_path, filename)
        if os.path.isfile(full_path):
            get_file(full_path, color_channel, binning, stream_id, stream_target)
        else:
            print(directory_path + filename + ' is not a file')
        time.sleep(period) # TODO: we haven't allocated any time since the last image was sent ?!
    print("simulator: all files streamed")


def get_file(file_path, color_channel, binning, stream_id, stream_target=None):
    """
    This function takes one file, checks if it has the correct color channel, reads and converts the file and
    sends it to the streaming framework.
    """
    file_name = os.path.basename(file_path)

    # In the AZ dataset, a particular character indicates the color channel:
    if color_channel is not None and file_name[-5] not in color_channel:
        return

    img = cv2.imread(file_path, -1)

    if binning is not None:
        # BB: this doesn't work with an ordinary PNG with 2 arguments in the block size.
        # BB: this seems to work on an ordinary image with 3 arguments - color channels?
        binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
    else:
        binned_img = img

    if stream_target is not None:
        # Convert image to bytes:
        ret, image_bytes_tiff = cv2.imencode('.tif', img_as_uint(binned_img))

        image_bytes_tiff = image_bytes_tiff.tobytes()
        print("file: {} has size: {}".format(file_path, len(image_bytes_tiff)))

        # print(topic)
        # print("prod: {} topic: {}".format(producer, topic))

        metadata = {
            'stream_id': stream_id,
            'timestamp': time.time(),
            'location': (12.34, 56.78),
            'image_length_bytes': len(image_bytes_tiff)
        }

        stream_target.send_message(image_bytes_tiff, file_name, metadata)
