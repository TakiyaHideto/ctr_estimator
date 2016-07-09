__author__ = 'Jiahao Dong'

import os

def transform_prediction(downsample_prediction, downsample_rate):
    origin_prediction = downsample_prediction / (downsample_prediction+(1-downsample_prediction)/downsample_rate)
    return origin_prediction

def read_file_list(file_list):
    for i in range(0,len(file_list)):
        yield file_list[i]

def create_new_prediction_file(prediction_file_list):
    prediction_file_num = len(prediction_file_list)
    new_file = []
    for i in range(0, prediction_file_num, 1):
        new_file.append('{}_origin'.format(prediction_file_list[i]))
    return new_file

def change_file_name(prediction_file_list, origin_pred_file_list):
    for i in range(0,len(prediction_file_list),1):
        os.remove(prediction_file_list[i])
        os.rename(origin_pred_file_list[i], prediction_file_list[i])

def calibrate(prediction_file_list):
    downsample_pred = read_file_list(prediction_file_list)
    origin_pred = read_file_list(create_new_prediction_file(prediction_file_list))
    while True:
        try:
            with open(origin_pred.next(), 'w') as fo:
                with open(downsample_pred.next(), 'r') as fi:
                    for prediction_result in fi:
                        prediction_result = float(prediction_result.rstrip('\n'))
                        origin_prediction = transform_prediction(prediction_result, downsample_rate=0.0116)
                        fo.write('{}\n'.format(origin_prediction))
        except StopIteration:
            print 'finish reading and transforming prediction results'
            break
    change_file_name(prediction_file_list, create_new_prediction_file(prediction_file_list))

if __name__ == '__main__':
    prediction_path = '/home/takiyahideto/Project/ttraining/result/prediction/prediction'
    prediction_file_list = []
    for i in range(0, 60, 1):
        prediction_file_list.append('{}{}'.format(prediction_path, i))
    calibrate(prediction_file_list)
