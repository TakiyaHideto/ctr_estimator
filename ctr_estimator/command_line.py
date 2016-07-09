__author__ = 'Jiahao Dong'

import configuration_file as cf

class Command(object):

    __learning_rate = 0.0
    __decay_rate = 0.0
    __l1 = 0.0
    __l2 = 0.0
    __ftrl_alpha = 0.0
    __ftrl_beta = 0.0
    __initial_weight = 0.0
    __bits_number = 0
    __display = 0
    training_parameters = {}


    def load_configuration_file(self):
        configure = cf.Configuration()
        configure.init_para()
        self.training_parameters = configure.get_training_parameters()
        # print training_parameters
        # return training_parameters

    def set_command_parameter(self):
        print 'Here you can set the training paratemer'
        self.load_configuration_file()
        self.__learning_rate = self.training_parameters['learning_rate']
        self.__decay_rate = self.training_parameters['decay_rate']
        self.__l1 = self.training_parameters['l1']
        self.__l2 = self.training_parameters['l2']
        self.__ftrl_alpha = self.training_parameters['ftrl_alpha']
        self.__ftrl_beta = self.training_parameters['ftrl_beta']
        self.__initial_weight = self.training_parameters['initial_weight']
        self.__bits_number = self.training_parameters['bit_number']
        self.__display = self.training_parameters['display_number']
        self.show_training_parameters()

    def show_training_parameters(self):
        print 'learning rate: {}'.format(self.__learning_rate)
        print 'decay rate: {}'.format(self.__decay_rate)
        print 'l1: {}'.format(self.__l1)
        print 'l2: {}'.format(self.__l2)
        print 'initial weight: {}'.format(self.__initial_weight)
        print 'bits number: {}'.format(self.__bits_number)
        print 'display number: {}'.format(self.__display)

    def get_commandline_train_all(self, train_set_vw, train_rounds, readable_model_file, predict_model_file,flag_first_round):
        if flag_first_round == False:
            commandline_train = 'vw {dataset} -i {model} -l {learn} --decay_learning_rate {decay} ' \
                                '--l1 {l1} --l2 {l2} --initial_t {initial} ' \
                                '--ftrl --ftrl_alpha {ftrl_alpha} --ftrl_beta {ftrl_beta} ' \
                                '-b {bits} --loss_function={loss} -P {display} -f {file}' \
                                ''.format(dataset=train_set_vw, model=predict_model_file, learn=self.__learning_rate,
                                          decay=self.__decay_rate, l1=self.__l1, l2=self.__l2,
                                          ftrl_alpha=self.__ftrl_alpha, ftrl_beta=self.__ftrl_beta,
                                          initial=self.__initial_weight, bits=self.__bits_number,
                                          loss="logistic", display=self.__display, file=predict_model_file)
        else:
            commandline_train = 'vw {dataset} -l {learn} --decay_learning_rate {decay} ' \
                                '--l1 {l1} --l2 {l2} --initial_t {initial} ' \
                                '--ftrl --ftrl_alpha {ftrl_alpha} --ftrl_beta {ftrl_beta} ' \
                                '-b {bits} --loss_function={loss} -P {display} -f {file}' \
                                ''.format(dataset=train_set_vw, learn=self.__learning_rate, decay=self.__decay_rate,
                                          l1=self.__l1, l2=self.__l2, initial=self.__initial_weight,
                                          ftrl_alpha=self.__ftrl_alpha, ftrl_beta=self.__ftrl_beta,
                                          bits=self.__bits_number, loss = "logistic",
                                          display=self.__display, file = predict_model_file)
        return commandline_train

    def get_commandline_train_single(self, train_set_vw, train_rounds, readable_model_file, predict_model_file, prediction_file):
        commandline_train = 'vw {dataset} -l {learn} --decay_learning_rate {decay} ' \
                            '--l1 {l1} --l2 {l2} --initial_t {initial} ' \
                            ' ' \
                            '-b {bits} --loss_function={loss} --link={link} ' \
                            '-P {display} -c --passes {passes} -f {file} ' \
                            '--save_per_pass --holdout_off' \
                            ''.format(dataset = train_set_vw, learn=self.__learning_rate, decay=self.__decay_rate,
                                      l1=self.__l1, l2=self.__l2, initial=self.__initial_weight,
                                      bits=self.__bits_number, loss="logistic", link="logistic",
                                      display=self.__display, passes=train_rounds, file=predict_model_file)
        return commandline_train

    def get_commandline_test_all(self, real_rounds, predict_model_file, test_set_vw, prediction_file):
        commandline_test = 'vw -i {model} -t -d {dataset} -p {predfile}' \
                           ''.format(model = predict_model_file, dataset = test_set_vw, predfile = prediction_file)
        return commandline_test

    def get_commandline_test_single(self, real_rounds, predict_model_file, test_set_vw, prediction_file):
        commandline_test = []
        for i in range(0,real_rounds,1):
            commandline_test.append('vw -i {model}.{round} -t {dataset} -p {predfile}{round}'
                                    ''.format(model = predict_model_file, round = i, dataset = test_set_vw, predfile = prediction_file))
        return commandline_test

    def save_invert_hash(self, train_set_vw, predict_model_file, readable_model_file, prediction_file):
        commandline_invert_hash = 'vw {dataset} -t -i {model} --invert_hash {model_file} -p {predfile}' \
                                  ''.format(dataset=train_set_vw, model=predict_model_file,
                                            predfile=prediction_file, model_file=readable_model_file)
        return commandline_invert_hash