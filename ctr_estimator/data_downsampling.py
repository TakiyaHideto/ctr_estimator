__author__ = 'Jiahao Dong'

import random

def check_positive_example(train_log_path):
    positive_example_counter = 0
    with open(train_log_path, 'r') as fi:
        for line in fi:
            element = line.rstrip('\n').split('\t')
            if element[0] is '1':
                positive_example_counter += 1
    return positive_example_counter

def split_example(train_log_path):
    positive_data = []
    negative_data = []
    with open(train_log_path, 'r') as fi:
        for line in fi:
            example = line
            element = line.rstrip('\n').split('\t')
            if element[0] is '1':
                positive_data.append(example)
            else:
                negative_data.append(example)
    return positive_data, negative_data

def check_positive_volume(positive_data):
    print len(positive_data)
    return len(positive_data)

def check_negative_volume(negative_data):
    return len(negative_data)

def generate_negative_index(positive_volume, negative_data, ratio):
    negative_index = set()
    negative_volume = check_negative_volume(negative_data)
    for i in range(0,positive_volume*ratio):
        while True:
            rand = random.randint(0,negative_volume)
            if rand not in negative_index:
                negative_index.add(rand)
                break
    return negative_index

def choose_negative_data(positive_data, negative_data, ratio):
    positive_volume = check_positive_volume(positive_data)
    negative_index = generate_negative_index(positive_volume, negative_data, ratio)
    new_negative_data = []
    for index in negative_index:
        new_negative_data.append(negative_data[index])
    return new_negative_data

def get_ratio():
    return 10

def merge_data(train_log_path):
    new_data = []
    positive_data, negative_data = split_example(train_log_path)
    ratio = get_ratio()
    negative_data = choose_negative_data(positive_data, negative_data, ratio)
    new_data.extend(positive_data)
    new_data.extend(negative_data)
    return new_data

def get_feature_name(train_log_path):
    with open(train_log_path, 'r') as fi:
        feature_name = fi.readline()
    return feature_name

def generate_new_train_log(train_log_path, new_log_path):
    new_data = merge_data(train_log_path)
    random.shuffle(new_data)
    with open(new_log_path, 'w') as fo:
        fo.write(get_feature_name(train_log_path))
        for line in new_data:
            fo.write(line)

if __name__ == '__main__':
    train_log_path = '/home/takiyahideto/Project/ctr_prediction_engine/data/all_date/train.log.txt'
    new_data_path = '/home/takiyahideto/Project/ctr_prediction_engine/data/all_date/down.train.log.txt'
    generate_new_train_log(train_log_path, new_data_path)