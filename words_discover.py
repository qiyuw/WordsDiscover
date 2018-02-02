# -*- coding: utf-8 -*
import numpy as np
import sys

def get_count_dict(string):
    c_list = list(string)
    c_set = set(c_list)
    c_dict = {i: c_list.count(i) for i in c_set}
    return c_dict

def get_information_entropy(c_list):
    total_freq = float(len(c_list))
    c_set = set(c_list)
    return np.sum([-(c_list.count(i)/total_freq) * np.log((c_list.count(i)/total_freq)) for i in c_set])

def get_mutual_information(string, real_tf):
    c_list = list(string)
    return np.log(real_tf / np.prod([C_COUNT_DICT[i] / STRING_L for i in c_list]))

def get_candidate_dict(string, min_l=2, max_l=5, tf=1, ie=0, pmi=1):
    """
    string: str (unicode)
    return: list
    """
    string_l = len(string)
    postfix_list = range(len(string))
    print len(postfix_list)
    postfix_list = sorted(postfix_list, cmp=lambda x, y: cmp(string[x:], string[y:]))
    print postfix_list[0]
    candidate_dict = {}
    total_freq = 0          
    for l in range(min_l, max_l + 1):
        last_word = None
        tmp_post_list = []
        tmp_pre_list = []
        tmp_tf = 0
        for i in postfix_list:
            if i + l > string_l:
                continue
            total_freq += 1
            word = string[i:i+l]
            postfix = string[i+l] if i + l < string_l else None
            prefix = string[i-1] if i - 1 >= 0 else None
            if word != last_word:
                candidate_dict.update({last_word: [tmp_tf, tmp_pre_list, tmp_post_list]})
                print last_word, tmp_tf
                last_word = word
            else:
                tmp_post_list.append(postfix)
                tmp_pre_list.append(prefix)
                tmp_tf += 1
    total_freq = float(total_freq)
    print "1 done"
    for i in candidate_dict:
        candidate_dict[i][1] = min(get_information_entropy(candidate_dict[i][1]), get_information_entropy(candidate_dict[i][2]))
        candidate_dict[i][2] = get_mutual_information(i, candidate_dict[i][0] / total_freq)
    print "2 done"
    candidate_list = sorted(candidate_dict.items(), lambda x, y: cmp(x[1][0] * (x[1][1] + x[1][2]), y[1][0] * (y[1][1] + y[1][2])), reverse=True)
    candidate_list = [i for i in candidate_list if i[1][0] > tf and i[1][1] > ie and i[1][2] > pmi]
    return candidate_list

if __name__ == "__main__":
    string = ""
    with open(sys.argv[1], 'r') as f:
        string = f.read()
    string = unicode(string, "utf-8")
    C_COUNT_DICT = get_count_dict(string)
    STRING_L = float(len(string))
    mylist = get_candidate_dict(string, min_l=2, max_l=2)
    for i in mylist[0:10]:
            print i[0], i[1]