__author__ = 'Jiahao Dong'

import time_consumed
import initialization
import one_hot as oh
import write_original_label as wol
import command_line as cl
import convert_to_prob as ctp
import train_test_model as ttm
import performance as ap
import write_redis as wr
import model_calibration as mc
import model_analysis as ma
import clear
import os
import time
import sys

class PredictionEngine(object):

    project_path = ''
    time_consumed = time_consumed.time_record()
    one_hot_object = oh.PreprocessData()
    command_object = object()

    def start(self):
        self.time_consumed.time_start = time.time()

    def process_train_data(self):
        print self.path_object.raw_train_file
        self.one_hot_object.one_hot_train_set(self.path_object.raw_train_file, self.path_object.train_set_vw,
                                              self.path_object.feature_index_file)
        self.time_consumed.time_process_train_data = time.time()

    def train_model(self):
        pass

    def process_test_data(self):
        self.one_hot_object.one_hot_test_set(self.path_object.raw_test_file, self.path_object.test_set_vw,
                                             self.path_object.feature_index_file)
        wol.get_original_label(self.path_object.test_set_vw, self.path_object.origin_testlables_file)
        self.time_consumed.time_process_test_data = time.time()

    def test_model(self):
        pass

    def plot_graph(self):
        pass

    def write_weight_redis(self):
        wr.write_to_database(self.path_object.readable_model_file)
        self.time_consumed.time_save_redis = time.time()

    def read_weight_redis(self):
        self.time_consumed.time_read_redis = time.time()

    def stop(self):
        self.time_consumed.time_stop = time.time()
        self.time_consumed.show_time()

    def set_command_parameter(self):
        self.command_object = cl.Command()
        self.command_object.set_command_parameter()

    def init_para(self, project_path_name):
        self.project_path = project_path_name

class PredictionEngineSingle(PredictionEngine):

    real_rounds = 0
    path_object = initialization.SingleSetInitialization()

    def start(self, project_path_name):
        self.time_consumed.time_start = time.time()
        self.init_para(project_path_name)
        self.path_object.init_para(self.project_path)
        self.set_command_parameter()
        self.one_hot_object.choose_data_set(data_name="ipinyou")

    def train_model(self):
        ttm.exe_train_model(self.command_object.get_commandline_train_single(self.path_object.train_set_vw,
                                                            self.path_object.train_rounds,
                                                            self.path_object.readable_model_file,
                                                            self.path_object.predict_model_file,
                                                            self.path_object.prediction_file))
        self.time_consumed.time_train = time.time()

    def test_model(self):
        self.real_rounds = self.get_real_rounds(self.path_object.model_path)
        ttm.exe_test_model_multipasses(self.command_object.get_commandline_test_single(self.real_rounds,
                                                                      self.path_object.predict_model_file,
                                                                      self.path_object.test_set_vw,
                                                                      self.path_object.prediction_file))
        self.time_consumed.time_test = time.time()

    def get_prediction_file_list(self):
        prediction_file_ist = []
        for i in range(0,self.real_rounds,1):
            prediction_file_ist.append('{}{}'.format(self.path_object.prediction_file, i))
        return prediction_file_ist

    def model_calibration(self):
        prediction_file_list = self.get_prediction_file_list()
        mc.calibrate(prediction_file_list)

    def plot_graph(self):
        prediction_set = []
        chart_flag = 'curve_single'
        for i in range(0,self.real_rounds,1):
            prediction_set.append('{0}{1}'.format(self.path_object.prediction_file, i))
        ap.auc_graph(self.path_object.origin_testlables_file, prediction_set,
                     self.path_object.figure_path, self.path_object.advertiser,
                     self.real_rounds, chart_flag, self.path_object.auc_file)
        self.time_consumed.time_plot = time.time()

    def select_best_model(self):
        ma.pick_best_model(self.path_object.auc_file, self.path_object.predict_model_file,
                           self.path_object.best_model_file)

    def save_feature_weights(self):
        ttm.exe_test_model(self.command_object.save_invert_hash(self.path_object.train_set_vw,
                                                                self.path_object.best_model_file,
                                                                self.path_object.readable_model_file,
                                                                self.path_object.prediction_file))

    def get_real_rounds(self, model_path):
        return len(os.popen("ls {0} | grep 'predict.model.[0-9]'".format(model_path)).readlines())

    def clear_file(self):
        for i in range(0,self.real_rounds,1):
            os.remove(self.path_object.predict_model_file + '.' + str(i))


class PredictionEngineMulti(PredictionEngine):

    path_object = initialization.MultiSetInitialization()
    real_rounds = 0  # this variable is not used by now, but it is worthy keep it
                     # it is used to record rounds that model has been trained due to holdout
    example_number = 0 # this means how many examples in a train log
    minibatch = 0.0
    head_line = ''   # this is the feature name (the first line in train log)
    auc_curve_list = [[] for i in range(0,9)] # this list is used to record every auc value for every advertiser.
                                              # there are at most 9 advertisers right now
    xlabels = [] # this is also mainly working for auc graph by recording advertiser names we want to test on
    sub_rounds = 0 # as the whole train log is too large to read all at one time, we can read part of it one by one
    flag_first_round = True # this means we don't need to read model to train at the first time
    advertiser_list = []

    def __set_example_number(self, raw_data_path):
        temp_arr = (os.popen('wc -l {0}train.log.txt'.format(raw_data_path)).readline().split(' '))
        self.example_number = int(temp_arr[0])
        print '{0} pieces of data'.format(self.example_number)

    def __set_head_line(self, raw_train_file):
        with open(raw_train_file) as file:
            self.head_line = file.readline()

    def __set_minibatch(self):
        print 'please set minibatch by input number of 1-9(million)'
        # temp1 = str(sys.stdin.readline().rstrip('\n'))
        temp1 = self.path_object.configure.get_mini_batch()
        temp2 = float('{0}e+6'.format(temp1))
        self.minibatch = float(temp2)
        print int(self.minibatch)

    def __set_sub_rounds(self):
        self.sub_rounds = int((self.example_number)/(self.minibatch) + 1)

    def __check_delete_sub_trainlog(self, sub_train_log):
        if os.path.isfile(sub_train_log):
            os.remove(sub_train_log)

    def perform_in_loop(self,project_path_name):
        self.start(project_path_name)
        for round_number in range(0,self.path_object.train_rounds,1):
            file_handle = open(self.path_object.raw_train_file,'r')
            line = file_handle.readline()
            for counter in range(0,self.sub_rounds,1):
                sub_raw_data_train = open(self.path_object.sub_raw_train_file, 'w')
                sub_raw_data_train.write(self.head_line)
                for i in range(0,int(self.minibatch),1):
                    line = file_handle.readline()
                    sub_raw_data_train.write(line)
                sub_raw_data_train.close()
                self.process_train_data()
                self.train_model()
                self.process_test_data()
                self.test_model()
                self.plot_graph(round_number, counter)
                self.select_best_model()
                self.save_feature_weights()
                self.write_weight_redis()
                self.read_weight_redis()
                self.flag_first_round = False

    def start(self, project_path_name):
        self.time_consumed.time_start = time.time()
        super(PredictionEngineMulti, self).init_para(project_path_name)
        self.path_object.init_para(self.project_path)
        self.init_para()
        self.__check_delete_sub_trainlog(self.path_object.sub_raw_train_file)
        self.set_command_parameter()
        self.one_hot_object.choose_data_set(data_name="ipinyou")

    def process_train_data(self):
        print 'start processing train log data'
        self.one_hot_object.one_hot_train_set(self.path_object.sub_raw_train_file, self.path_object.train_set_vw,
                                              self.path_object.feature_index_file)
        os.remove(self.path_object.sub_raw_train_file)
        self.time_consumed.time_process_train_data = time.time()

    def train_model(self):
        print 'start traing model'
        ttm.exe_train_model(self.command_object.get_commandline_train_all(self.path_object.train_set_vw,
                                                         self.path_object.train_rounds,
                                                         self.path_object.readable_model_file,
                                                         self.path_object.predict_model_file,
                                                         self.flag_first_round))
        # ttm.exe_test_model(self.command_object.save_invert_hash(self.path_object.train_set_vw,
        #                                        self.path_object.predict_model_file,
        #                                        self.path_object.readable_model_file, self.path_object.prediction_file))
        self.time_consumed.time_train = time.time()

    def process_test_data(self):
        print 'start processing test log data'
        for i in range(0,len(self.path_object.test_set_name),1):
            if os.path.isfile(self.path_object.test_set_vw[i]) != True:
                self.one_hot_object.one_hot_test_set(self.path_object.raw_test_file[i],
                                                     self.path_object.test_set_vw[i],
                                                     self.path_object.feature_index_file)
                wol.get_original_label(self.path_object.test_set_vw[i],
                                       self.path_object.original_testlabels_file[i])
        self.time_consumed.time_process_test_data = time.time()

    def test_model(self):
        print 'start testing model'
        for i in range(0,len(self.path_object.test_set_name),1):
            ttm.exe_test_model(self.command_object.get_commandline_test_all(self.real_rounds,
                                                           self.path_object.predict_model_file,
                                                           self.path_object.test_set_vw[i],
                                                           self.path_object.prediction_file[i]))
            ctp.convert_to_probability(self.path_object.prediction_file[i],
                                       self.path_object.original_testlabels_file[i])
        self.time_consumed.time_test = time.time()

    def plot_bar(self, round_number, counter):
        print self.path_object.test_set_name
        ap.auc_graph(self.path_object.original_testlabels_file,
                     self.path_object.prediction_file,
                     self.path_object.result_path,
                     self.path_object.test_set_name,
                     round_number*5+counter, 'bar')

    def plot_curve(self, round_number, counter):
        y_auc = ap.calc_auc_list(self.path_object.original_testlabels_file,
                                 self.path_object.prediction_file,
                                 self.path_object.test_set_name)
        for i in range(0,len(self.path_object.test_set_name),1):
            self.auc_curve_list[i].append(y_auc[i])
        self.xlabels.append(round_number*self.sub_rounds+counter+1)
        if round_number>0 and (counter%5  ==  0):
            ap.plot_curve_all(self.xlabels,self.auc_curve_list,self.path_object.test_set_name,
                              self.path_object.result_path,
                              round_number*5+counter)

    def plot_graph(self, round_number, counter):
        print 'start ploting graph'
        self.plot_bar(round_number, counter)
        self.plot_curve(round_number, counter)
        self.time_consumed.time_plot = time.time()

    def select_best_model(self):
        ma.pick_best_model(self.path_object.auc_file, self.path_object.predict_model_file,
                           self.path_object.best_model_file)

    def save_feature_weights(self):
        ttm.exe_test_model(self.command_object.save_invert_hash(self.path_object.train_set_vw,
                                                                self.path_object.best_model_file,
                                                                self.path_object.readable_model_file,
                                                                self.path_object.prediction_file))

    def init_para(self):
        self.__set_example_number(self.path_object.raw_data_path)
        self.__set_head_line(self.path_object.raw_train_file)
        self.__set_minibatch()
        self.__set_sub_rounds()
        print 'finish initializing'

class PredictionMG(PredictionEngine):

    real_rounds = 0
    path_object = initialization.MGInitialization()

    def start(self, project_path_name):
        self.time_consumed.time_start = time.time()
        self.init_para(project_path_name)
        self.path_object.init_para(self.project_path)
        self.one_hot_object.choose_data_set(data_name="mg")
        self.set_command_parameter()

    def train_model(self):
        ttm.exe_train_model(self.command_object.get_commandline_train_single(self.path_object.train_set_vw,
                                                            self.path_object.train_rounds,
                                                            self.path_object.readable_model_file,
                                                            self.path_object.predict_model_file,
                                                            self.path_object.prediction_file))
        self.time_consumed.time_train = time.time()

    def test_model(self):
        self.real_rounds = self.get_real_rounds(self.path_object.model_path)
        ttm.exe_test_model_multipasses(
            self.command_object.get_commandline_test_single(self.real_rounds,
                                                            self.path_object.predict_model_file,
                                                            self.path_object.test_set_vw,
                                                            self.path_object.prediction_file))
        self.time_consumed.time_test = time.time()

    def get_prediction_file_list(self):
        prediction_file_ist = []
        for i in range(0,self.real_rounds,1):
            prediction_file_ist.append('{}{}'.format(self.path_object.prediction_file, i))
        return prediction_file_ist

    def model_calibration(self):
        configure = self.path_object.get_configure()
        if configure.get_signal_downsampling() == 'yes':
            prediction_file_list = self.get_prediction_file_list()
            mc.calibrate(prediction_file_list)

    def plot_graph(self):
        prediction_set = []
        chart_flag = 'curve_single'
        for i in range(0,self.real_rounds,1):
            prediction_set.append('{0}{1}'.format(self.path_object.prediction_file, i))
        ap.auc_graph(self.path_object.origin_testlables_file, prediction_set,
                     self.path_object.figure_path, self.path_object.date,
                     self.real_rounds, chart_flag, self.path_object.auc_file)
        self.time_consumed.time_plot = time.time()

    def select_best_model(self):
        ma.pick_best_model(self.path_object.auc_file, self.path_object.predict_model_file,
                           self.path_object.best_model_file)

    def save_feature_weights(self):
        ttm.exe_test_model(self.command_object.save_invert_hash(self.path_object.train_set_vw,
                                                                self.path_object.best_model_file,
                                                                self.path_object.readable_model_file,
                                                                self.path_object.prediction_file))

    def get_real_rounds(self, model_path):
        return len(os.popen("ls {0} | grep 'predict.model.[0-9]'".format(model_path)).readlines())

    def clear_file(self):
        clear.clear_predict_model(self.path_object.predict_model_file, self.real_rounds)
