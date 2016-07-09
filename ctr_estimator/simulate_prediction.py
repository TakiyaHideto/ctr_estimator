__author__ = 'Jiahao Dong'

import redis
import json
import time
import math

def predict_from_json(json_file_path):
    predict_linear = 0.0
    fea_arr = []
    start = time.time()
    connection = redis.Redis(db=1)

    with open(json_file_path, 'r') as file:
        for line in file:
            decode_json = json.loads(line.rstrip('\n'))

            fea_arr.append('Constant')
            fea_arr.append('IP@' + str(decode_json['device']['ip']))
            fea_arr.append('region@' + str(decode_json['device']['geo']['region']))
            fea_arr.append('city@' + str(decode_json['device']['geo']['city']))
            fea_arr.append('adexchange@' + str(decode_json['ext']['adexchange']))
            fea_arr.append('domain@' + str(decode_json['site']['domain']))
            fea_arr.append('slot@' + str(decode_json['imp'][0]['banner']['id']))
            fea_arr.append('slot@' + str(decode_json['imp'][0]['banner']['w']))
            fea_arr.append('slot@' + str(decode_json['imp'][0]['banner']['h']))
            fea_arr.append('creative@' + str(decode_json['ext']['creativeid']))
            # add feature ...

            for feature in fea_arr:
                if connection.exists(feature):
                    predict_linear += float(connection.get(feature))

            predict_probability = (1/(1+math.exp(-predict_linear)))
            print "Click probability is {} ".format(predict_probability)

            predict_linear = 0.0
            fea_arr = []

        stop = time.time()
        print "{} millisecond consumed from receiving to giving a prediction".format(stop - start)

if __name__ == "__main__":
    json_file_path = '../../make-ipinyou-data/json_test/data-test1000.json.txt'
    predict_from_json(json_file_path)