import os

import numpy as np
from PIL import Image

file_path = "09AssayPlate_NUNC_#165305-1_F05_T0038F002L01A02Z01C01.tif"

# file_path = "D:\Bibliotek\Documents\Exjobb\Bilder-20171019T090142Z-001\Bilder\AssayPlate_NUNC_#165305-1_B02_T0001F001L01A01Z01C02.tif"

print(os.path.isfile(file_path))
m = file_path
m1 = file_path
m2 = file_path
m3 = file_path

list_im = [m, m1, m2, m3]

imgs = [Image.open(i) for i in list_im]
# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]

imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

# save that beautiful picture
imgs_comb = Image.fromarray(imgs_comb)
imgs_comb.save('D:\Bibliotek\Documents\Exjobb\Bilder-20171019T090142Z-001\Bilder\Trifecta.tif')

# im.save("D:\Bibliotek\Documents\Exjobb\Bilder-20171019T090142Z-001\Bilder\estIMG.tif")
