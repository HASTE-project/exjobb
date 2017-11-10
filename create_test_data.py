# Create new datasets for testing the simulator with images of different sizes

import os
import cv2
import numpy as np
from skimage.measure import block_reduce


def create_test_images(file_path, binning):
    files = os.listdir(file_path)
    original_size = []
    size_after_binning = []
    if not os.path.exists(file_path + str(binning)):
        os.mkdir(file_path + str(binning))
    for file in files:
        if os.path.isfile(file_path + file):
            img = cv2.imread(file_path + file, -1)
            binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
            binned_img = binned_img.astype(np.uint16)
            cv2.imwrite(file_path + str(binning) + "/binned_" + file, binned_img)
            original_size.append(os.path.getsize(file_path + file))
            size_after_binning.append(os.path.getsize(file_path + str(binning) + "/binned_" + file))
        else:
            pass
    sum_org_size = sum(list(original_size))
    sum_size_after_bin = sum(size_after_binning)
    print(len(original_size))
    try:
        print(sum_size_after_bin/sum_org_size)
    except ZeroDivisionError:
        print(sum_org_size)
        print(sum_size_after_bin)


create_test_images("D:\Bibliotek\Documents\Exjobb\Bilder-20171019T090142Z-001\Bilder/",1)
create_test_images("D:\Bibliotek\Documents\Exjobb\Bilder-20171019T090142Z-001\Bilder/",2)
create_test_images("D:\Bibliotek\Documents\Exjobb\Bilder-20171019T090142Z-001\Bilder/",3)
create_test_images("D:\Bibliotek\Documents\Exjobb\Bilder-20171019T090142Z-001\Bilder/",4)
create_test_images("D:\Bibliotek\Documents\Exjobb\Bilder-20171019T090142Z-001\Bilder/",5)
create_test_images("D:\Bibliotek\Documents\Exjobb\Bilder-20171019T090142Z-001\Bilder/",6)
