__author__ = 'Jiahao Dong'

import os

def exe_train_model(command):
    os.popen(command)
    print '-------finish training model-------'

def exe_test_model(command):
    os.popen(command)
    print '-------finish testing model--------'

def exe_test_model_multipasses(command):
    for c in command:
        os.popen(c)
    print '-------finish testing model--------'