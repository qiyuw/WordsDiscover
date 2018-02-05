# -*- coding: utf-8 -*
import numpy as np
import pygtrie as trie
import sys
import datetime

def l_in_s(l, s):
    l = [unicode(i, 'utf-8') for i in l]
    for i in l:
        if i in s:
            return True
    return False

def get_count_dict(string):
    start = datetime.datetime.now()
    print "start create count_dict ...".upper()
    c_dict = trie.StringTrie()
    for c in string:
        if c in c_dict:
            c_dict[c] += 1
        else:
            c_dict[c] = 1
    end = datetime.datetime.now()
    print ("create count_dict done, costs time: %s" % (str(end - start))).upper()
    return c_dict   

def get_information_entropy(c_list):
    total_freq = float(len(c_list))
    c_set = set(c_list)
    return np.sum([-(c_list.count(i)/total_freq) * np.log((c_list.count(i)/total_freq)) for i in c_set])

def get_mutual_information(string, real_tf):
    c_list = list(string)
    return np.log(real_tf / np.prod([C_COUNT_DICT[i] / STRING_L for i in c_list]))

def get_candidate_dict(string, min_l=2, max_l=5, tf=1, ie=0, pmi=1, exclu_list=['\n', ' ', '：', '。', '“', '”', '！', '？']):
    """
    string: str (unicode)
    return: list
    """
    string_l = len(string)
    print ("text length: %d" % (string_l)).upper()
    postfix_list = range(len(string))
    candidate_dict = trie.StringTrie()
    total_freq = 0
    start = datetime.datetime.now()
    print "start create candidate_dict ...".upper()          
    for l in range(min_l, max_l + 1):
        # last_word = string[postfix_list[0]:postfix_list[0]+l]
        # tmp_post_list = []
        # tmp_pre_list = []
        # tmp_tf = 0
        for i in postfix_list:
            if i + l > string_l:
                continue
            total_freq += 1
            word = string[i:i+l]
            if l_in_s(exclu_list, word):
                continue
            postfix = string[i+l] if i + l < string_l else None
            prefix = string[i-1] if i - 1 >= 0 else None
            if word in candidate_dict:
                candidate_dict[word][0] += 1
                candidate_dict[word][1].append(prefix)
                candidate_dict[word][2].append(postfix)
            else:
                candidate_dict[word] = [1, [], []]
    total_freq = float(total_freq)
    end = datetime.datetime.now()
    print ("create candidate_dict done, costs time: %s" % (str(end - start))).upper()
    start = datetime.datetime.now()
    print "start computing information entropy and mutual information ...".upper()
    for i in candidate_dict:
        candidate_dict[i][1] = min(get_information_entropy(candidate_dict[i][1]), get_information_entropy(candidate_dict[i][2]))
        candidate_dict[i][2] = get_mutual_information(i, candidate_dict[i][0] / total_freq)
    end = datetime.datetime.now()
    print ("computing done, costs time: %s" % (str(end - start))).upper()
    candidate_list = [(i, candidate_dict[i]) for i in candidate_dict if candidate_dict[i][0] > tf and candidate_dict[i][1] > ie and candidate_dict[i][2] > pmi]    
    candidate_list = sorted(candidate_list, lambda x, y: cmp(x[1][0] * (x[1][1] + x[1][2]), y[1][0] * (y[1][1] + y[1][2])), reverse=True)
    return candidate_list

if __name__ == "__main__":
    string = ""
    with open(sys.argv[1], 'r') as f:
        string = f.read()
    string = unicode(string, "utf-8")
    C_COUNT_DICT = get_count_dict(string)
    STRING_L = float(len(string))
    mylist = get_candidate_dict(string, min_l=2, max_l=5)
    for i in mylist[0:10]:
            print i[0], i[1]