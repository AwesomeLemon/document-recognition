from __future__ import print_function
import cv2
import numpy as np
from crop import crop
from scan import scan
import pytesseract
from PIL import Image
import argparse
from test_accuracy import test_accuracy

def recognize(imgname='photos\\bad2.jpg', output='output.txt', desired='chom_tough.txt'):
    # construct the argument parser and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True,
    #                 help="Path to the image to be scanned")
    # ap.add_argument("-o", "--output", required=True,
    #                 help="Path for the output text file")
    # ap.add_argument("-c", "--check", required=True,
    #                 help="Path to the file with reference text")
    # args = vars(ap.parse_args())
    scan(imgname, False)

    img = cv2.imread('res.jpg')
    img = cv2.dilate(img, np.ones((2, 2)))
    newimgname = 'no_noise.jpg'
    cv2.imwrite(newimgname, img)
    crop(newimgname, "scan_res.jpg", False)
    a = pytesseract.image_to_string(Image.open('scan_res.jpg'), config="config")
    f = open(output, 'w+')
    print (a, file=f)
    f.flush()
    f.close()
    # print (test_accuracy())
    print(test_accuracy(scan_res=output, desired=desired))

def recognize_many(img_names_file):
    with open(img_names_file) as f:
        names = f.readlines()
    names = [x.strip() for x in names]
    for name in names:
        output = name + 'output.txt'
        desired = 'chom.txt'
        if 'tough' in name:
            desired = 'chom_tough.txt'
        elif 'bad' in name:
            desired = 'bad.txt'
        elif 'ital' in name:
            desired = 'ital.txt'
        elif 'font1' in name:
            desired = 'font1.txt'
        elif 'font2' in name:
            desired = 'font2.txt'
        print ('\n' + name)
        recognize(name, output, desired)

recognize_many('photos.txt')