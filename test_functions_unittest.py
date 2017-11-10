import unittest
import cv2
import numpy as np
from skimage.measure import block_reduce
from simulator import get_files
import simulatorNoFlask
import os

class TestGetFiles(unittest.TestCase):
    """Tests for get_files"""
    # def test_block_reduce_function(self):
    #     assert(os.path.isfile('D:\\Bibliotek\Documents\Exjobb\Bilder - 20171019T090142Z-001\Bilder/AssayPlate_NUNC_#165305-1_B02_T0001F001L01A01Z01C02.tif'))
    #     img = cv2.imread(
    #         'D:\\Bibliotek\Documents\Exjobb\Bilder - 20171019T090142Z-001\Bilder/AssayPlate_NUNC_#165305'
    #         '-1_B02_T0001F001L01A01Z01C02.tif', -1)
    #     binned_img = block_reduce(img, block_size=(1, 1), func=np.sum)
    #     np.array_equal(img, binned_img)

    def test_get_files(self):
#        file_path = "D:\Bibliotek\Documents\Exjobb\Bilder-20171019T090142Z-001\Bilder"
        file_path = "/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/"
        frequency = 1
        binning = 2
        color_channel = [1]
        connect_kafka = "No"
        simulatorNoFlask.time_get_files(file_path, frequency, binning, color_channel, connect_kafka)

    def test_test_timeit(self):
        simulatorNoFlask.timer('test.json')


if __name__ == '__main__':
    unittest.main()
