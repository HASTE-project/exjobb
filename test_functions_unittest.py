import unittest
from _ctypes import sizeof


import cv2
import numpy as np
from skimage.measure import block_reduce
#import simulator
#import simulatorNoFlask
import os
import create_test_data
import profiling
from PIL import Image
from skimage import img_as_ubyte
from skimage import img_as_int
from skimage import img_as_uint
from skimage import img_as_float
import io
import binascii
from io import StringIO
from io import BytesIO



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
        file_path = "D:\Bibliotek\Documents\Exjobb\Bilder-20171019T090142Z-001\Bilder"
        #file_path = "/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/"
        frequency = 1
        binning = 2
        color_channel = [1]
        connect_kafka = "No"
        profiling.time_get_files(file_path, frequency, binning, color_channel, connect_kafka)

    def test_test_timeit(self):
        profiling.timer('test.json')

    def test_save_img(self):
        #in producer
        imgfile = cv2.imread("D:\\Bibliotek\\Documents\\Exjobb\\Bilder-20171019T090142Z-001\\Bilder/AssayPlate_NUNC_#165305-1_B02_T0001F001L01A01Z01C02.tif", -1)
        print("type imgfile: {}".format(type(imgfile)))
        print("imgfile size: {}".format(imgfile.shape))
        binned_img = block_reduce(imgfile, block_size=(1, 1), func=np.sum)

        print("binned_img type: {}".format(type(binned_img)))
        print("binned_img size: {}".format(binned_img.shape))

        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
        print("jpeg type: {}".format(type(jpeg)))
        print("jpeg size: {}".format(jpeg.shape))
        img_bytes = jpeg.tobytes()
        print("img_bytes type: {}".format(type(img_bytes)))



        #in consumer
        img = cv2.imdecode(np.frombuffer(img_bytes, dtype=np.uint16), -1)
        print("type img : {}".format(type(img)))
        print("size img: {}".format(img.shape))
        fin2 = Image.fromarray(img)
        print("fin2 type: {}".format(type(fin2)))
        fin2.save("fin22.tif")

        assert (np.array_equal(img, imgfile))

    def test_simulator_get_files(self):
        file_path = '/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/'
        frequency = 1
        binning = 1
        color_channel = ['1', '2', '3']
        connect_kafka = 'yes'
        simulator.get_files(file_path, frequency, binning, color_channel, connect_kafka)

 


    # def test_create_test_data(self):
    #     create_test_data.create_test_images("C:\\Users\Lovisa\exjobb\\testData/", 3)
    #     print(os.path.getsize("testData\AssayPlate_NUNC_#165305-1_B02_T0001F001L01A01Z01C02.tif"))
    #     print(os.path.getsize("bild.tif"))



if __name__ == '__main__':
    unittest.main()
