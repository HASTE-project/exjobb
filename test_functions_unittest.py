import unittest
import cv2
import numpy as np
from PIL import ImageChops
from skimage.measure import block_reduce
from simulator import get_files

class TestGetFiles(unittest.TestCase):
    """Tests for get_files"""
    def test_block_reduce_function(self):

        img = cv2.imread(
            'D:\\Bibliotek\Documents\Exjobb\Bilder - 20171019T090142Z-001\Bilder/AssayPlate_NUNC_#165305'
            '-1_B02_T0001F001L01A01Z01C02.tif', -1)
        binned_img = block_reduce(img, block_size=(1, 1), func=np.sum)
        np.array_equal(img, binned_img)

    def test_get_files(self):
        file_path = "D:\\Bibliotek\Documents\Exjobb\Bilder - 20171019T090142Z-001\Bilder/"
        frequency = 1
        binning = 2
        color_channel = ['red', 'green']
        get_files(file_path, frequency, binning, color_channel)


if __name__ == '__main__':
    unittest.main()