from __future__ import division

import jellyfish


def test_accuracy(scan_res='output.txt', desired='texts\\chom.txt'):
    return jaro_dist(scan_res, desired)


def get_file_as_string(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return ''.join(content)


def jaro_dist(scan_res='output.txt', desired='texts\\chom.txt'):
    scan_line = get_file_as_string(scan_res)
    desired_line = get_file_as_string(desired)
    return jellyfish.jaro_winkler(scan_line.decode("utf-8"), desired_line.decode("utf-8"), long_tolerance=True)


# print jaro_dist()
