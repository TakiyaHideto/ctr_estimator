__author__ = 'Jiahao Dong'

import engine
import os

def perform_single_set():
    path_tmp = os.path.abspath(os.path.join(os.path.dirname('__file__'),os.path.pardir))
    project_path = '{0}/'.format(os.path.abspath(os.path.join(path_tmp,os.path.pardir)))

    media_gamma = engine.PredictionEngineSingle()
    media_gamma.start(project_path)
    media_gamma.process_train_data()
    media_gamma.train_model()
    media_gamma.process_test_data()
    media_gamma.test_model()
    media_gamma.model_calibration()
    media_gamma.plot_graph()
    media_gamma.select_best_model()
    media_gamma.save_feature_weights()
    media_gamma.write_weight_redis()
    media_gamma.read_weight_redis()
    media_gamma.stop()

def perform_multi_set():
    path_tmp = os.path.abspath(os.path.join(os.path.dirname('__file__'),os.path.pardir))
    project_path = '{0}/'.format(os.path.abspath(os.path.join(path_tmp,os.path.pardir)))

    media_gamma = engine.PredictionEngineMulti()
    media_gamma.perform_in_loop(project_path)

def perform_mg():
    path_tmp = os.path.abspath(os.path.join(os.path.dirname('__file__'),os.path.pardir))
    project_path = '{0}/'.format(os.path.abspath(os.path.join(path_tmp,os.path.pardir)))

    media_gamma = engine.PredictionMG()
    media_gamma.start(project_path)
    media_gamma.process_train_data()
    media_gamma.train_model()
    media_gamma.process_test_data()
    media_gamma.test_model()
    media_gamma.model_calibration()
    media_gamma.plot_graph()
    media_gamma.select_best_model()
    media_gamma.save_feature_weights()
    media_gamma.write_weight_redis()
    media_gamma.read_weight_redis()
    media_gamma.stop()
    media_gamma.clear_file()