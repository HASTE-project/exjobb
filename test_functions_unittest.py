import unittest
from _ctypes import sizeof


import cv2
import numpy as np
from skimage.measure import block_reduce
#from simulator import get_files
import simulatorNoFlask
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
        imgfile = cv2.imread("D:\\Bibliotek\\Documents\\Exjobb\\Bilder-20171019T090142Z-001\\Bilder/AssayPlate_NUNC_#165305-1_B02_T0001F001L01A01Z01C02.tif", -1)
        print("type imgfile: {}".format(type(imgfile)))
        print("imgfile size: {}".format(imgfile.shape))
        binned_img = block_reduce(imgfile, block_size=(1, 1), func=np.sum)
        # print(imgfile)
        #
        # print(binned_img)
        print("binned_img type: {}".format(type(binned_img)))
        print("binned_img size: {}".format(binned_img.shape))
        #cv2.imwrite("testInt.tiff", img_as_int(binned_img))
        cv2.imwrite("testUint.tiff", img_as_uint(binned_img))
        #cv2.imwrite("testFloat.tiff", img_as_float(binned_img))
#         print("img_as_ubyte type: {}".format(type(img_as_ubyte(binned_img))))
#         print("img_as_ubyte size: {}".format(img_as_ubyte(binned_img).shape))
        ret, jpeg = cv2.imencode('.tif', img_as_uint(binned_img))
        print("jpeg type: {}".format(type(jpeg)))
        print("jpeg size: {}".format(jpeg.shape))
        img_bytes = jpeg.tobytes()
        print("img_bytes type: {}".format(type(img_bytes)))
#
#         # yield (b'--frame\r\n'
#         #        b'Content-Type: image/tiff\r\n\r\n' + img_bytes + b'\r\n\r\n')
#
        # stream = img_bytes # io.BytesIO(img_bytes)
        # print(type(stream))
        # img = Image.open(stream)
        # img.save(os.path.join(os.path.expanduser('~'), "testTest1.tiff"))
#         import scipy.misc
        #st = img_bytes.decode("utf-8")
        img_hex = img_bytes.hex()
        print("img_hex type: {}".format(type(img_hex)))
        data = np.fromstring(img_hex, dtype=np.uint8)
        print("data type: {}".format(type(data)))
        print("data size: {}".format(data.shape))

        im = Image.open(BytesIO(img_bytes))
        print("im type: {}".format(type(im)))
        print("im size: {}".format(im.size))
        print(im)
        im.save("im.tiff")

        # im2 = Image.open(np.fromstring(img_hex))
        # print("im2 type: {}".format(type(im2)))
        # print("im2 size: {}".format(im2.size))
        # print(im2)
        # im.save("im2.tiff")
        # Image.frombytes('I', (1234, 1034), b'--frame\r\n'
        # b'Content-Type: image/tif\r\n\r\n' + img_bytes + b'\r\n\r\n')
        fin = Image.fromarray(binned_img)
        print("fin type: {}".format(type(fin)))
        fin.save("fin.tiff")
#
        #
        # print(b'--frame\r\n'
        # b'Content-Type: image/tif\r\n\r\n' + img_bytes + b'\r\n\r\n')
#
#         image_data = img_bytes  # byte values of the image
#         image = Image.open(io.BytesIO(image_data))
#         image.save(os.path.join(os.path.expanduser('~'), "test.tiff"))
#
#
#         print(type(image_data))
#        # print(image_data.shape)
#
# #        print(dir(image_data))
#        # print(sizeof(image_data))
#         # img = Image.open(stream)
#         # img.save(os.path.join(os.path.expanduser('~'), "test.tiff"))
#
        img = cv2.imdecode(np.fromstring(img_hex, dtype=np.uint8), -1)
        print("type img : {}".format(type(img)))
        np.save('testet.tif', img)
#
#         img_str = img_bytes.hex()
#         nparr = np.fromstring(img_str, np.uint8)
#         img_np = cv2.imdecode(nparr, 0)
#         print("type nparr: {}".format(type(nparr)))
#         print("type img_np: {}".format(type(img_np)))
#
#
#         Image.fromarray(jpeg).save("outfile2.tif") # scipy.misc.toimage(binned_img, cmin=0.0, cmax=1).save('outfile.jpg')
#
#     # def test_create_test_data(self):
#     #     create_test_data.create_test_images("C:\\Users\Lovisa\exjobb\\testData/", 3)
#     #     print(os.path.getsize("testData\AssayPlate_NUNC_#165305-1_B02_T0001F001L01A01Z01C02.tif"))
#     #     print(os.path.getsize("bild.tif"))


if __name__ == '__main__':
    unittest.main()
