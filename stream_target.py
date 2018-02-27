import abc

class StreamTarget:

    @abc.abstractmethod
    def send_message(self, image_bytes, file_name, metadata):
        """
        :param image_bytes: bytearray for image.
        :param file_name: original file name of image.
        :param metadata: extra information (timestamp, spatial information, unique stream ID, etc.)
        :return:
        """
        raise NotImplementedError('users must define this method to use this base class')

