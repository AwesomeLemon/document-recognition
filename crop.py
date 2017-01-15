import cv2
import util

import numpy as np

imshow = False


def props_for_contours(contours, ary):
    """Calculate bounding box & the number of set pixels for each contour."""
    c_info = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        c_im = np.zeros(ary.shape)
        cv2.drawContours(c_im, [c], 0, 255, -1)
        c_info.append({
            'x1': x,
            'y1': y,
            'x2': x + w - 1,
            'y2': y + h - 1,
            'sum': np.sum(ary * (c_im > 0)) / 255
        })
    return c_info


def union_crops(crop1, crop2):
    x11, y11, x21, y21 = crop1
    x12, y12, x22, y22 = crop2
    return min(x11, x12), min(y11, y12), max(x21, x22), max(y21, y22)


def find_border_components(contours, ary):
    borders = []
    area = ary.shape[0] * ary.shape[1]
    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        if w * h > 0.5 * area:
            borders.append((i, x, y, x + w - 1, y + h - 1))
    return borders


def find_components(edges, max_components=10):
    # Dilate the image until there are just a few connected components.
    count = max_components + 1
    n = 1
    components = None
    while count > max_components:
        n += 1
        dilated_image = cv2.dilate(edges / 255, np.ones((3, 3)), iterations=n)
        components = cv2.connectedComponentsWithStats(dilated_image)
        count = components[0]
    if imshow:
        cv2.imshow("Edged", util.resize(edges, height=650))
        cv2.imshow("Edged dilated", util.resize(255 * dilated_image, height=650))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return components


def find_number_of_text_pixels_in_crop(img, crop):
    res = 0
    for j in range(crop['x1'], crop['x2']):
        for i in range(crop['y1'], crop['y2']):
            if img[i][j] > 0:
                res += 1
    crop['sum'] = res
    return crop


def find_optimal_components_subset(components, edges):
    total = np.sum(edges / 255)
    c_info = components_properties(components, edges)

    c_info.sort(key=lambda x: -x['sum'])

    c = c_info[0]
    del c_info[0]
    this_crop = c['x1'], c['y1'], c['x2'], c['y2']
    crop = this_crop
    covered_sum = c['sum']

    for i, c in enumerate(c_info):
        this_crop = c['x1'], c['y1'], c['x2'], c['y2']
        if covered_sum / float(total) < 0.9:
            # print '%d %s -> %s' % (i, covered_sum, covered_sum + c['sum'])
            crop = union_crops(crop, this_crop)
            covered_sum += c['sum']
        else:
            break

    return crop


def components_properties(components, edges):
    c_info = []
    for i in range(1, components[0]):
        cur_comp = components[2][i]
        crop = {'x1': cur_comp[0], 'y1': cur_comp[1], 'x2': cur_comp[0] + cur_comp[2] - 1,
                'y2': cur_comp[1] + cur_comp[3] - 1, 'sum': cur_comp[4]}
        crop = find_number_of_text_pixels_in_crop(edges, crop)
        c_info.append(crop)
    return c_info


def crop(path, out_path, show=False):
    global imshow
    imshow = show
    orig_im = cv2.imread(path)
    downscaled_height = 600.0
    scale = orig_im.shape[0] / downscaled_height
    im = util.resize(orig_im, height=int(downscaled_height))

    edges = cv2.Canny(im, 30, 200)
    edges = 255 * (edges > 0).astype(np.uint8)
    edges_blurred = cv2.medianBlur(edges, 5)

    components = find_components(edges_blurred)
    if components[0] == 0:
        print '%s -> (no text!)' % path
        return
    crop = find_optimal_components_subset(components, edges)

    crop = [int(x * scale) for x in crop]  # upscale to the original image size.
    orig_im = orig_im[crop[1]:crop[3], crop[0]: crop[2]]
    cv2.imwrite(out_path, orig_im)

# crop("no_noise.jpg", "scan_res.jpg", True)
