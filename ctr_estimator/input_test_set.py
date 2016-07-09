__author__ = 'Jiahao Dong'
import sys
import os

def input_test(data_path, test_dataset):
    flag = True
    test_set = []
    while flag:
        print 'test_set: {}'.format(get_all_single_test_name(data_path))
        print "Please input file name splitted by ',' "
        input_file = test_dataset
        file_name = input_file.rstrip('\n').split(',')
        for i in file_name:
            test_set.append(int(i))
        test_set, flag = check_set(set(test_set), flag)
        print test_dataset
    return test_set

def check_set(input_set, flag):
    test_set = set([1458, 2259, 2261, 2821, 2997, 3358, 3386, 3427, 3476])
    advertiser_list = []
    if len(input_set-test_set) == 0:
            flag = False
            for i in input_set:
                advertiser_list.append(i)
    else:
        print 'Wrong! Please input corret file name again'
        advertiser_list = []
    return advertiser_list, flag

def get_all_single_test_name(data_path):
    test_set = []
    name_set = os.popen('ls {} | grep [0-9][0-9][0-9][0-9]'.format(data_path)).readlines()
    for element in name_set:
        test_set.append(element.strip())
    return test_set

