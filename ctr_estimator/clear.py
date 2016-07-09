__author__ = 'Jiahao Dong'

import os

# These functions are used to clear some intermediate file generated in the course of training
# This file has not been completed

def clear_predict_model(predict_model_file, rounds):
    for i in range(0,rounds,1):
        os.remove(predict_model_file + '.' + str(i))

def clear_train_vw_set(train_set_vw):
    os.remove(train_set_vw)

def clear_train_vw_set_cache(train_set_vw_cache):
    os.remove(train_set_vw_cache)

def clear_test_vw_set(test_set_vw):
    os.remove(test_set_vw)

def clear_prediction_file(prediction_file, real_rounds):
    for i in range(0,real_rounds-1):
        os.remove('{}{}'.format(prediction_file, i))

if __name__ == '__main__':
    print os.getcwd()