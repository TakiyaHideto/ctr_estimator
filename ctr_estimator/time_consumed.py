__author__ = 'Jiahao Dong'

class time_record:
    # all the time variable records the end point
    time_start = 0.0
    time_process_train_data = 0.0
    time_train = 0.0
    time_process_test_data = 0.0
    time_test = 0.0
    time_plot = 0.0
    time_save_redis = 0.0
    time_read_redis = 0.0
    time_stop = 0.0

    __period_process_train_data = 0.0
    __period_train = 0.0
    __period_process_test_data = 0.0
    __period_test = 0.0
    __period_plot = 0.0
    __period_save_redis = 0.0
    __period_read_redis = 0.0
    __period_total = 0.0

    def show_time(self):
        self.__calc_time()
        print '---------------------------------------------\n' \
              'time of processing train data: {0}m {1}s'.format(int(self.__period_process_train_data / 60),int(self.__period_process_train_data % 60))
        print '---------------------------------------------\n' \
              'time of training: {0}m {1}s'.format(int(self.__period_train / 60), int(self.__period_train % 60))
        print '---------------------------------------------\n' \
              'time of processing testing data: {0}m {1}s'.format(int(self.__period_process_test_data / 60), int(self.__period_process_test_data % 60))
        print '---------------------------------------------\n' \
              'time of testing: {0}m {1}s'.format(int(self.__period_test / 60), int(self.__period_test % 60))
        print '---------------------------------------------\n' \
              'time of ploting graph: {0}m {1}s'.format(int(self.__period_plot / 60), int(self.__period_plot % 60))
        print '---------------------------------------------\n' \
              'time of saving data to redis: {0}m {1}s'.format(int(self.__period_save_redis / 60), int(self.__period_save_redis % 60))
        print '---------------------------------------------\n' \
              'time of reading data from redis: {0}m {1}s'.format(int(self.__period_read_redis / 60), int(self.__period_read_redis % 60))
        print '---------------------------------------------\n' \
              'time of the whole process: {0}m {1}s'.format(int(self.__period_total / 60), int(self.__period_total % 60))

    def __calc_time(self):
        self.__period_process_train_data = self.time_process_train_data - self.time_start
        self.__period_train = self.time_train - self.time_process_train_data
        self.__period_process_test_data = self.time_process_test_data - self.time_train
        self.__period_test = self.time_test - self.time_process_test_data
        self.__period_plot = self.time_plot - self.time_test
        self.__period_save_redis = self.time_save_redis - self.time_plot
        self.__period_read_redis = self.time_read_redis - self.time_save_redis
        self.__period_total = self.time_stop - self.time_start