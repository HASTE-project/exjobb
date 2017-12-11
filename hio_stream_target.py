from kafka_stream_target import StreamTarget
from stream_connector import StreamConnector # see: https://github.com/beirbear/HarmonicSC
import pickle


class HarmonicIOStreamTarget(StreamTarget):
    """
    Sends messages (tasks) to the Harmonic IO master.
    """

    def __init__(self, hio_master_host, hio_port):
        self.sc = StreamConnector(hio_master_host, hio_port)

    def send_message(self, image_bytes, image_file_name, metadata):
        """
        :param image_bytes: bytearray or bytes for image.
        :param file_name: original file name of image.
        :param metadata: extra information (timestamp, spatial information, unique stream ID, etc.)
        :return:
        """
        # The format of this binary blob is specific to the image analysis code.
        # TODO: add link!
        pickled_metadata = bytearray(pickle.dumps(metadata))

        message = pickled_metadata + image_bytes
        self.sc.send_data(message)
