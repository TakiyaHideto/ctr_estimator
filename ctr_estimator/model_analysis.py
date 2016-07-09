__author__ = 'Jiahao Dong'

import shutil

def get_highest_auc(auc_file):
    auc_highest = 0.0
    index = -1
    with open(auc_file, 'r') as file:
        for line in file:
            auc = float(line.rstrip('\n'))
            if auc > auc_highest:
                auc_highest = auc
                index += 1
    return auc_highest, index

def pick_best_model(auc_file, predict_model_file, best_model_file):
    auc_highest, index = get_highest_auc(auc_file)
    shutil.copyfile('{}.{}'.format(predict_model_file, index), best_model_file)

def calculate_average_ctr(prediction_file):
    counter = 0
    ctr_sum = 0.0
    with open(prediction_file, 'r') as file:
        for line in file:
            ctr_sum += float(line.rstrip('\n'))
            counter += 1
    return float(ctr_sum/counter)

def analyse_user_id(readable_model_path):
    with open(readable_model_path) as file:
        for line in file:
            if line.strip().startswith('user_id'):
                parts = line.strip().split(':')
                if float(parts[2]) > 0.1:
                    print '{}\t{}'.format(parts[0],parts[2])

# def user_id_click_number(data_path):
#     user_click = {}
#     with open(data_path, 'r') as file:
#         for line in file:
#
#
# if __name__ == "__main__":
#     readable_model_path = '/home/takiyahideto/Project/ctr_prediction_engine/result2015-08-07_04:07/predict_model/readable_model'
#     analyse_user_id(readable_model_path)