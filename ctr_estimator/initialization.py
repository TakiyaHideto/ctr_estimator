__author__ = 'Jiahao Dong'

import input_test_set as its
import sys
import os
import time
import configuration_file as cf

class PathInitialization(object):

    data_path = ''
    code_path = ''
    raw_data_path = ''
    result_path = ''
    figure_path = ''
    model_path = ''
    prediction_path = ''
    ctr_test_path = ''

    train_set_vw = ''
    feature_index_file = ''
    origin_trainlabels_file = ''
    predict_model_file = ''
    readable_model_file = ''
    best_model_file = ''
    ctr_test_json = ''
    auc_file = ''

    configure = object()

    def set_dir_path_parent(self, project_path):
        self.data_path = '{0}data/'.format(project_path)
        self.code_path = '{0}ctr_estimator/'.format(project_path)
        self.result_path = '{0}result{1}/'.format(project_path,time.strftime("%F_%H:%M"))
        self.figure_path = '{0}figure/'.format(self.result_path)
        self.model_path = '{0}predict_model/'.format(self.result_path)
        self.prediction_path = '{0}prediction/'.format(self.result_path)
        self.ctr_test_path = '{0}json_test/'.format(self.data_path)

    def set_file_path_parent(self):
        self.train_set_vw = '{0}train_vw.txt'.format(self.result_path)
        self.feature_index_file = '{0}feature_index_file.txt'.format(self.result_path)
        self.origin_trainlabels_file = '{0}label_train.txt'.format(self.result_path)
        self.predict_model_file = '{0}predict.model'.format(self.model_path)
        self.readable_model_file = '{0}readable_model'.format(self.model_path)
        self.best_model_file = '{0}best_model'.format(self.model_path)
        self.ctr_test_json = '{0}data-test1000.txt'.format(self.ctr_test_path)
        self.auc_file = '{0}auc.txt'.format(self.result_path)

    def check_creat_path(self):
        path_array = [self.result_path, self.model_path, self.prediction_path, self.figure_path]
        for path in path_array:
            if not os.path.isdir(path):
                os.mkdir(path)

    def set_configure(self):
        self.configure = cf.Configuration()
        self.configure.init_para()

    def get_configure(self):
        return self.configure

    def init_para(self, project_path):
        self.set_dir_path_parent(project_path)
        self.check_creat_path()
        self.set_file_path_parent()


class SingleSetInitialization(PathInitialization):

    advertiser = ''
    train_rounds = 0
    raw_data_path = ''
    raw_train_file = ''
    raw_test_file = ''
    test_set_vw = ''
    origin_testlables_file = ''
    prediction_file = ''

    def choose_single_testset(self):
        print 'choose one of advertisers: 1458, 2259, 2261, 2821, 2997, 3358, 3386, 3427, 3476'
        # self.advertiser = int(sys.stdin.readline().strip())
        configure = self.get_configure()
        self.advertiser = (configure.get_dataset())
        print '{}'.format(self.advertiser)

    def set_train_rounds(self):
        print 'input train rounds'
        # self.train_rounds = int(sys.stdin.readline().strip())
        configure = self.get_configure()
        self.train_rounds = configure.get_training_rounds()
        print '{}'.format(self.train_rounds)

    def set_dir_path(self, project_path):
        self.choose_single_testset()
        self.raw_data_path = '{0}{1}/'.format(self.data_path, self.advertiser)

    def set_file_path(self):
        configure = self.get_configure()
        if configure.get_signal_downsampling() == 'yes':
            self.raw_train_file = '{0}down.train.log.txt'.format(self.raw_data_path)
        else:
            self.raw_train_file = '{0}train.log.txt'.format(self.raw_data_path)
        self.raw_test_file = '{0}test.log.txt'.format(self.raw_data_path)
        self.test_set_vw = '{0}test_vw.txt'.format(self.result_path)
        self.origin_testlables_file = '{0}label_test.txt'.format(self.result_path)
        self.prediction_file = '{0}prediction'.format(self.prediction_path)

    def init_para(self, project_path):
        super(SingleSetInitialization,self).init_para(project_path)
        self.set_configure()
        self.set_dir_path(project_path)
        self.set_file_path()
        self.set_train_rounds()


class MultiSetInitialization(PathInitialization):
    
    train_rounds = 0
    advertiser = ''
    
    raw_data_path = ''
    raw_train_file = ''
    sub_raw_train_file = ''
    raw_test_file = []
    test_set_name = []
    test_set_vw = []
    original_testlabels_file = []
    prediction_file = []
    
    def choose_multi_testset(self):
        self.advertiser = 'all'
        configure = self.get_configure()
        self.test_set_name = its.input_test(self.data_path, configure.get_test_dataset())
        
    def set_train_rounds(self):
        print 'input train rounds'
        configure = self.get_configure()
        # self.train_rounds = int(sys.stdin.readline().strip())
        self.train_rounds = configure.get_training_rounds()
        print '{}'.format(self.train_rounds)
    
    def set_dir_path(self, project_path):
        self.choose_multi_testset()
        self.raw_data_path = '{0}{1}/'.format(self.data_path, self.advertiser)
        
    def set_file_path(self):
        self.raw_train_file = '{0}train.log.txt'.format(self.raw_data_path)
        self.sub_raw_train_file = '{0}sub.train.log.txt'.format(self.result_path)
        for i in self.test_set_name:
            self.raw_test_file.append(self.data_path + str(i) + '/' + 'test.log.txt')
        for i in self.test_set_name:
            self.test_set_vw.append(self.result_path + 'testset_vw' + str(i) + '.txt')
        for i in self.test_set_name:
            self.original_testlabels_file.append(self.result_path + 'label_testSet' + str(i) + '.txt')
        for i in self.test_set_name:
            self.prediction_file.append(self.prediction_path + 'prediction' + str(i))

    def init_para(self, project_path):
        super(MultiSetInitialization,self).init_para(project_path)
        self.set_configure()
        self.set_dir_path(project_path)
        self.set_file_path()
        self.set_train_rounds()


class MGInitialization(PathInitialization):

    date = ''
    train_rounds = 0
    raw_data_path = ''
    raw_train_file = ''
    raw_test_file = ''
    test_set_vw = ''
    origin_testlables_file = ''
    prediction_file = ''

    def choose_single_testset(self):
        print 'Input the date like 2015-**-** or "all_date" '
        # self.date = (sys.stdin.readline().strip())
        configure = self.get_configure()
        self.date = (configure.get_dataset())
        print '{}'.format(self.date)

    def set_train_rounds(self):
        print 'input train rounds'
        # self.train_rounds = int(sys.stdin.readline().strip())
        configure = self.get_configure()
        self.train_rounds = configure.get_training_rounds()
        print '{}'.format(self.train_rounds)

    def set_dir_path(self, project_path):
        self.choose_single_testset()
        self.raw_data_path = '{0}{1}/'.format(self.data_path, self.date)

    def set_file_path(self):
        configure = self.get_configure()
        if configure.get_signal_downsampling() == 'yes':
            self.raw_train_file = '{0}down.train.log.txt'.format(self.raw_data_path)
        else:
            self.raw_train_file = '{0}train.log.txt'.format(self.raw_data_path)
        self.raw_test_file = '{0}test.log.txt'.format(self.raw_data_path)
        self.test_set_vw = '{0}test_vw.txt'.format(self.result_path)
        self.origin_testlables_file = '{0}label_test.txt'.format(self.result_path)
        self.prediction_file = '{0}prediction'.format(self.prediction_path)

    def init_para(self, project_path):
        super(MGInitialization,self).init_para(project_path)
        self.set_configure()
        self.set_dir_path(project_path)
        self.set_file_path()
        self.set_train_rounds()