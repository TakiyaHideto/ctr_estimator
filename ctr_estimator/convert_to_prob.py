__author__ = 'Jiahao Dong'

import math

def convert_to_probability(prediction_file,origin_labels_test):
    prediction_results = []
    labels = []
    with open(prediction_file, 'r') as file:
        for line in file:
            prediction_results.append(float(line.rstrip('\n')))
    with open(origin_labels_test, 'r') as file:
        for line in file:
            if (line.rstrip(('\n'))) == '-1':
                labels.append(-1)
            else:
                labels.append(1)
    with open(prediction_file, 'w') as file:
        for i in range(0,len(prediction_results),1):
           probability = 1.0/(1.0+math.exp(-float(prediction_results[i])))
           probability_round = round(probability,5)
           file.write(str(probability_round)+'\n')