from __future__ import division

import itertools
import difflib
import jellyfish
from sklearn.feature_extraction.text import TfidfVectorizer

def tf_idf(scan_res='output.txt', desired='chom.txt'):
    # documents = [open(f) for f in text_files]
    tfidf = TfidfVectorizer().fit_transform([open(scan_res), open(desired)])
    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = tfidf * tfidf.T
    print pairwise_similarity

def test_accuracy(scan_res='output.txt', desired='chom.txt'):
    return jaro_dist(scan_res, desired)
    scan_words = get_word_list(scan_res)
    desired_words = get_word_list(desired)
    good = 0
    total = 0
    scanned_num = len(scan_words)
    desired_num = len(desired_words)
    if scanned_num == desired_num:
        for i in range(scanned_num):
            good += common_chars_num(scan_words[i], desired_words[i])
            total += len(desired_words[i])
    else:
        sc_i = 0
        des_i = 0
        while sc_i < scanned_num and des_i < desired_num:
            desired_word = desired_words[des_i]
            cur_coinc = common_chars_num(scan_words[sc_i], desired_word)
            scan_union = scan_words[sc_i]
            if cur_coinc == len(desired_word) or len(desired_word) != 2 and not (cur_coinc < 0.5 * len(desired_word) and cur_coinc < 3):
                good += cur_coinc
                total += len(desired_word)
                sc_i += 1
                des_i += 1
                continue
            found_good = False
            #try to match next:
            if sc_i + 1 < scanned_num and des_i + 1 < desired_num:
                nxt_desired_word = desired_words[des_i + 1]
                nxt_coinc = common_chars_num(scan_words[sc_i + 1], desired_word)
                scan_union = scan_words[sc_i + 1]
                if nxt_coinc == len(nxt_desired_word) or len(nxt_desired_word) != 2 and not (
                        nxt_coinc < 0.5 * len(nxt_desired_word) and nxt_coinc < 3):
                    good += nxt_coinc + cur_coinc
                    total += len(desired_word) + len(nxt_desired_word)
                    sc_i += 2
                    des_i += 2
                    continue
            while cur_coinc < 0.5 * len(desired_words[des_i]) and cur_coinc < 3:
                sc_i += 1
                if sc_i >= scanned_num:
                    break
                scan_union += scan_words[sc_i]
                # there're (probably) less scanned words than desired.

                old_des_i = -1
                for i in range(des_i, min(desired_num, des_i + 5)):
                    cur_coinc = common_chars_num(scan_union, desired_words[i])
                    if cur_coinc > 0.5 * len(desired_words[i]) and cur_coinc > 1:
                        old_des_i = des_i
                        des_i = i
                        found_good = True
                        break
                if (found_good):
                    for i in range(old_des_i, des_i + 1):
                        total += len(desired_words[i])
                    good += cur_coinc

                    break

            if not found_good:
                total += len(desired_words[des_i])
            sc_i += 1
            des_i += 1

    print (good / total)


def common_chars_num(word1, word2):
    i = 0
    minlen = min(len(word1), len(word2))
    while i < minlen and word1[i] == word2[i]:
        i += 1
    res = i
    seq_matcher = difflib.SequenceMatcher(None, word1, word2)
    return max(res, seq_matcher.find_longest_match(i, len(word1), i, len(word2)).size)


def get_word_list(file):
    words = []
    for line in open(file):
        line = line.rstrip('\n')
        if line:
            words.extend(line.split(' '))

    return words

def get_file_as_string(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return ''.join(content)

def jaro_dist(scan_res='output.txt', desired='chom.txt'):
    scan_line = get_file_as_string(scan_res)
    desired_line = get_file_as_string(desired)
    return jellyfish.jaro_winkler(scan_line.decode("utf-8"), desired_line.decode("utf-8"), long_tolerance=False)

print jaro_dist()
# print get_file_as_string('chom.txt')
# print common_chars_num('0ccupy', 'occ432cupy')
# test_accuracy()
# test_accuracy(desired='chom_tough.txt')
# tf_idf(desired='chom_tough.txt')