from __future__ import print_function
import cv2
import numpy as np
from crop import crop
from scan import scan
import pytesseract
from PIL import Image

from test_accuracy import test_accuracy

scan("tough7.jpg", False)

img = cv2.imread('res.jpg')
# img = cv2.medianBlur(img,3)
img = cv2.dilate(img, np.ones((2, 2)))
# img = cv2.erode(img,np.ones((2, 2)))
newimgname = 'no_noise.jpg'
cv2.imwrite(newimgname, img)
crop(newimgname, "scan_res.jpg", False)
a = pytesseract.image_to_string(Image.open('scan_res.jpg'), config="config")
f = open('output.txt', 'w+')
print (a, file=f)
f.flush()
f.close()
# print (test_accuracy())
print(test_accuracy(desired='chom_tough.txt'))