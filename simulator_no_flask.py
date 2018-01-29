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
import azn_filenames

import cv2
import numpy as np
from skimage import img_as_uint
from skimage.measure import block_reduce

from hio_stream_target import HarmonicIOStreamTarget


def get_files(image_directory_path, period, binning, color_channel_filter, send_to_target, hio_config=None,
              stream_id_tag='ll'):
    """
    This function retrieves files and creates a stream of files to be used as a microscope simulator.
    :param image_directory_path: path to directory containing image test data set files
    :param period: The time period between every image (setting to 0 gives minimal time period)
    :param binning: specify the binning (reduce the number of pixels to compress the image), this is given as an
    int. Or 'None' to use the original image.
    :param color_channel_filter: filter files according to color channels to send (according to AZ convention), the channels
    are given as a list eg. ['1', '2'] (the Yokogawa microscope can have up to five color channels).
    Or 'None' to include all files.
    :param send_to_target: specify if the simulator shall stream images somewhere else with streaming framework
    :param hio_config: configuration dict for HarmonicIO integration. (see: hio_stream_target.py)
    :param stream_id_tag: string to use in stream ID
    """
    files = os.listdir(image_directory_path)
    files = [file for file in files if not file.startswith('.')]
    print("simulator: list of files to stream:")
    print(files)

    stream_id = datetime.datetime.today().strftime('%Y_%m_%d__%H_%M_%S') + '_' + stream_id_tag
    print("simulator: stream ID is: " + stream_id)

    stream_target = None
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

    files = {filename: azn_filenames.parse_azn_file_name(filename) for filename in files}

    # Add full path:
    for filename in files:
        files[filename]['full_path'] = os.path.join(image_directory_path, filename)

    # Filter on color channel:
    if color_channel_filter is not None:
        files = {filename: file_info for filename, file_info in files.items()
                 if file_info['color_channel'] in color_channel_filter}

    # TODO: group into set of images with all colors, and send as a single message.

    for filename, file_info in files.items():
        __stream_file(filename, file_info, binning, stream_id, stream_target)
        time.sleep(period)  # TODO: we haven't allocated any time since the last image was sent ?!

    print("simulator: all files streamed")


def __stream_file(file_name, file_metadata, binning, stream_id, stream_target=None):
    # take one file, read, convert and send to the streaming framework.

    image_bytes_tiff = __prepare_image_bytes(binning, file_metadata)
    print("file: {} has size: {}".format(file_name, len(image_bytes_tiff)))

    file_metadata['stream_id'] = stream_id,
    file_metadata['timestamp'] = time.time(),
    file_metadata['location'] = (12.34, 56.78),
    file_metadata['image_length_bytes'] = len(image_bytes_tiff),
    file_metadata['original_filename'] = file_name

    if stream_target is not None:
        # print(topic)
        # print("prod: {} topic: {}".format(producer, topic))
        stream_target.send_message(image_bytes_tiff, file_name, file_metadata)


def __prepare_image_bytes(binning, file_metadata):
    img = cv2.imread(file_metadata['full_path'], -1)

    if binning is not None:
        # BB: this doesn't work with an ordinary PNG with 2 arguments in the block size.
        # BB: this seems to work on an ordinary image with 3 arguments - color channels?
        binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
    else:
        binned_img = img

    # Convert image to bytes:
    ret, image_bytes_tiff = cv2.imencode('.tif', img_as_uint(binned_img))

    image_bytes_tiff = image_bytes_tiff.tobytes()
    return image_bytes_tiff
