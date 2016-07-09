__author__ = 'Jiahao Dong'

import json

class Configuration(object):

    configuration_file_path = ''
    configuration_para = {}

    def init_para(self):
        self.configuration_file_path = '../../configuration'
        self.set_configuration()

    def set_configuration(self):
        with open(self.configuration_file_path, 'r') as file_read:
            for line in file_read:
                elements = line.rstrip('\n').split('=')
                self.configuration_para[elements[0]] = elements[1]

    def get_configuration(self):
        return self.configuration_para

    def get_engine_number(self):
        configure_para = self.get_configuration()
        return int(configure_para['engine_number'])

    def get_dataset(self):
        configure_para = self.get_configuration()
        # dataset = configure_para['dataset'].split(',')
        dataset = str(configure_para['dataset'])
        return dataset

    def get_training_rounds(self):
        configure_para = self.get_configuration()
        return int(configure_para['training_rounds'])

    def get_training_parameters(self):
        configure_para = self.get_configuration()
        training_parameters = json.JSONDecoder().decode(configure_para['training_parameters'])
        return training_parameters

    def get_test_dataset(self):
        configure_para = self.get_configuration()
        return configure_para['test_dataset']

    def get_mini_batch(self):
        configure_para = self.get_configuration()
        return int(configure_para['mini_batch'])

    def get_signal_downsampling(self):
        configure_para = self.get_configuration()
        return configure_para['downsampling']

# if __name__ == '__main__':
#     configuration_file_path = '../configuration'
#     conf = Configuration(configuration_file_path)
#     train_para = conf.get_training_parameters()
#     print train_para['decay_rate']