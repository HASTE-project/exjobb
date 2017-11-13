# Create new datasets for testing the simulator with images of different sizes

import os
import cv2
import numpy as np
import shutil
from skimage.measure import block_reduce


def create_test_images(source, dest, binning):
    files = os.listdir(source)
    original_size = []
    size_after_binning = []
    if not os.path.exists(dest + str(binning)):
        os.mkdir(dest + str(binning))
    for file in files:
        if os.path.isfile(source + file):
            img = cv2.imread(source + file, -1)
            binned_img = block_reduce(img, block_size=(binning, binning), func=np.sum)
            binned_img = binned_img.astype(np.uint16)
            cv2.imwrite(dest + str(binning) + "/binned_" + file, binned_img)
            for i in range(499):
                shutil.copy2(dest + str(binning) + "/binned_" + file,
                             dest + str(binning) + "/binned_" + str(i) + file)
            original_size.append(os.path.getsize(source + file))
            size_after_binning.append(os.path.getsize(dest + str(binning) + "/binned_" + file))
            break
        else:
            pass

    sum_org_size = sum(list(original_size))
    sum_size_after_bin = sum(size_after_binning)

    try:
        fo = open("file_information.txt", "a")
        fo.write("\n Binning: {} ".format(binning))
        fo.write("\n sum_size_after_bin/sum_org_size: {}".format(sum_size_after_bin/sum_org_size))
        fo.write("\n original_size: {}".format(original_size))
        fo.write("\n size_after_binning: {}".format(size_after_binning))
        fo.write("\n")
        fo.close()
        print(sum_size_after_bin/sum_org_size)
    except ZeroDivisionError:
        print(sum_org_size)
        print(sum_size_after_bin)


#create_test_images("/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/",
#                   "/mnt/volume2//testDatasets/", 1)
#create_test_images("/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/",
#                   "/mnt/volume2//testDatasets/",2)
#create_test_images("/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/",
#                   "/mnt/volume2//testDatasets/",3)
#create_test_images("/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/",
#                   "/mnt/volume2//testDatasets/",4)
#create_test_images("/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/",
#                   "/mnt/volume2//testDatasets/",5)
#create_test_images("/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/",
#                   "/mnt/volume2//testDatasets/",6)


def org_file(source, dest):
	file = "AssayPlate_NUNC_#165305-1_F05_T0038F002L01A02Z01C01.tif"
	for i in range(500):
		shutil.copy2(source + file, dest + "0" + str(i) + file)

org_file("/mnt/volume/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1/",
                   "/mnt/volume2//testDatasets/0/")
