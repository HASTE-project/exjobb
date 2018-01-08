from kafka_stream_target import StreamTarget
from harmonicIO.stream_connector.stream_connector import StreamConnector
import pickle


class HarmonicIOStreamTarget(StreamTarget):
    """
    Sends messages (tasks) to the Harmonic IO master.
    Supports the version with containers, at: https://github.com/beirbear/HarmonicIO/tree/CI_v0_r1/stream_connector

    IP addresses of workers are in the private subnet, so this client only works from inside the cloud.
    """

    def __init__(self, config):
        """
        :param config: dict containing config params, eg.:
        {
            'master_host':'192.168.12.34',
            'master_port':8080,
            'container_name':'hakanwie/test:batch_hist2',
            'container_os':'ubuntu'
        }
        """

        self.config = config

        self.sc = StreamConnector(self.config['master_host'], self.config['master_port'], max_try=1, std_idle_time=1)

    def send_message(self, image_bytes_tiff, image_file_name, metadata):
        """
        :param image_bytes_tiff: bytearray or bytes for image.
        :param image_file_name: original file name of image.
        :param metadata: extra information (timestamp, spatial information, unique stream ID, etc.)
        :return:
        """

        # The format of this binary blob is specific to the image analysis code.
        # TODO: add link!
        pickled_metadata = bytearray(pickle.dumps(metadata))

        message_bytes = pickled_metadata + image_bytes_tiff

        self.sc.send_data(self.config['container_name'],
                          self.config['container_os'],
                          message_bytes)
