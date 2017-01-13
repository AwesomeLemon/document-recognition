# coding=utf-8
# import the necessary packages
import util
from transform import four_point_transform
from skimage.filters import threshold_adaptive
import argparse
import cv2


def scan(imgname="chom4.jpg", show=True):
    # construct the argument parser and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True,
    #                 help="Path to the image to be scanned")
    # args = vars(ap.parse_args())

    path = imgname #args["image"]
    image = cv2.imread(path)
    ratio = image.shape[0] / 700.0
    orig = image.copy()
    image = util.resize(image, height=700)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edged = cv2.Canny(gray, 40, 150)


    print "STEP 1: Edge Detection"

    edged_copy = edged.copy()
    edged_copy = cv2.GaussianBlur(edged_copy, (3, 3), 0)

    if show:
        cv2.imshow("Edged", edged)
        cv2.imshow("Edged blurred", edged_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    (_, cnts, _) = cv2.findContours(edged_copy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:4]

    screenCnt = []

    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        # approx = np.array(cv2.boundingRect(c))
        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        debugging = False
        if debugging:
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
            cv2.imshow("Outline", image)
            cv2.waitKey(0)
        if len(approx) == 4:
            screenCnt = approx
            break
    if screenCnt.__len__() != 0:
        print "STEP 2: Find contours of paper"
        if show:
            cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
            cv2.imshow("Outline", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    else:
        warped = orig

    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    warped = threshold_adaptive(warped, 251, offset=10)
    warped = warped.astype("uint8") * 255

    # show the original and scanned images
    print "STEP 3: Apply perspective transform"
    if show:
        cv2.imshow("Original", util.resize(orig, height=650))
        cv2.imshow("Scanned", util.resize(warped, height=650))
        cv2.waitKey(0)
    cv2.imwrite('res.jpg', warped)
# scan()
