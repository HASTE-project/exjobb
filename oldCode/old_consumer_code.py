# imgfile = BytesIO(message.value)
# img = Image.open(imgfile)
# img.save(os.path.join(os.path.expanduser('~'), str(message.offset) + ".tiff"))


# with open(os.path.join(os.path.expanduser('~'), str(message.offset) + ".bin"), 'wb+') as f:
#     f.write(b'Content-Type: image/png\r\n\r\n' + message.value + b'\r\n\r\n')

# cv2.imwrite(os.path.join(os.path.expanduser('~'), str(message.offset) + ".png"), imag)

#      f = open("test.txt","a") #opens file with name of "test.txt"
#     f.write("\n offset: {} ".format(message.offset))

#    f.close()

# print(message.value)
#    for message in consumer:
# This will wait and print messages as they become available
# print('Offset: %s' % message.offset)
#       return 'Offset: %s' % message.aoffset