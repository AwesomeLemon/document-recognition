# coding=utf-8
import util
from transform import four_point_transform
from skimage.filters import threshold_local
import cv2


def scan(im_path, show=True):
    im = cv2.imread(im_path)
    orig = im.copy()

    downscaled_height = 700.0
    im, scale = util.downscale(im, downscaled_height)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    kern_size = 5
    gray_blurred = cv2.medianBlur(gray, kern_size)

    threshold_lower = 40
    threshold_upper = 150
    edged = cv2.Canny(gray_blurred, threshold_lower, threshold_upper)

    edged_copy = edged.copy()
    edged_copy = cv2.GaussianBlur(edged_copy, (3, 3), 0)

    cv2.imwrite('edged.jpg', edged)
    if show:
        cv2.imshow('Edged', edged)
        cv2.imshow('Edged blurred', edged_copy)
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
        # can assume that we have found our target
        debugging = False
        if debugging:
            cv2.drawContours(im, [approx], -1, (0, 255, 0), 2)
            cv2.imshow('Outline', im)
            cv2.waitKey(0)
        if len(approx) == 4:
            screenCnt = approx
            break
    if screenCnt.__len__() != 0:
        if show:
            cv2.drawContours(im, [screenCnt], -1, (0, 255, 0), 2)
            cv2.imwrite('outlined.jpg', im)
            cv2.imshow('Outline', im)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * scale)
    else:
        warped = orig

    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    warped = warped > threshold_local(warped, 251, offset=10)
    warped = warped.astype('uint8') * 255

    if show:
        cv2.imshow('Original', util.resize(orig, height=650))
        cv2.imshow('Scanned', util.resize(warped, height=650))
        cv2.waitKey(0)
    cv2.imwrite('deskewed.jpg', warped)
# scan()
