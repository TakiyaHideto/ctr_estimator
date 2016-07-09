__author__ = 'Jiahao Dong'

import operator
import os
import random
class PreprocessData(object):

    counter = 0
    __oses = []
    __browsers = []
    __f1s = []
    __f1sp = []
    __f2s = []

    def choose_data_set(self, data_name):
        flag = data_name
        try:
            {
                "ipinyou": self.ipinyou_dataset_fea_name,
                "mg": self.mg_dataset_fea_name,
            }[flag]()
        except KeyError:
            exit(1)

    def ipinyou_dataset_fea_name(self):
        self.__oses = ["windows", "ios", "mac", "android", "linux"]
        self.__browsers = ["chrome", "sogou", "maxthon", "safari", "firefox", "theworld", "opera", "ie"]
        self.__f1s = ["weekday", "hour", "IP", "region", "city", "adexchange", "domain", "slotid",
                      "slotwidth", "slotheight", "slotvisibility", "slotformat", "creative", "advertiser"]
        self.__f1sp = ["useragent", "slotprice"]
        self.__f2s = ["weekday,region"]

    def mg_dataset_fea_name(self):
        # self.__f1s = ['ad_tag_id','ad_id','ad_width','strategy_id','flight_id','campaign_id',
        #               'browser','os','device','ad_height','source','exchange_id','page_domain']
        self.__f1s = ['ad_tag_id','ad_id','ad_width','strategy_id','flight_id','campaign_id',
                      'browser','os','device','ad_height','source','exchange_id']

    def show_progress(self, process_name):
        if self.counter % 5000000 is 0:
            print 'read and process {} {}'.format(self.counter,process_name)
        self.counter += 1

    def reset_counter(self):
        self.counter = 0

    def transform_useragent(self, content):
        operation = "other"
        for o in self.__oses:
            if o in content:
                operation = o
                break
        browser = "other"
        for b in self.__browsers:
            if b in content:
                browser = b
                break
        return operation + "_" + browser

    def transform_slotprice(self, content):
        price = int(content)
        if price > 100:
            return "101+"
        elif price > 50:
            return "51-100"
        elif price > 10:
            return "11-50"
        elif price > 0:
            return "1-10"
        else:
            return "0"

    def feature_trainsform(self, name, content):
        content = content.lower()
        try:
            return {
                'useragent': self.transform_useragent,
                'slotprice': self.transform_slotprice,
            }[name](content)
        except KeyError:
            print 'KeyError'

    def process_usertags(self, namecol, data_element, feature_index, max_index):
        col = namecol["usertag"]
        tags = self.get_tags(data_element[col])
        for tag in tags:
            feat = str(col) + ':' + tag
            if feat not in feature_index:
                feature_index[feat] = max_index
                max_index += 1

    def get_tags(self, content):
        if content is '\n' or len(content) is 0:
            return ["null"]
        return content.strip().split(',')

    def is_file_empty(self, file_path):
        if os.path.isfile(file_path):
            return True
        else:
            return False

    def load_feature_from_old_file(self, feature_index_file,first,is_flag_true):
        max_index = 0
        feature_index = {}
        if os.path.isfile(feature_index_file):
            with open(feature_index_file, 'r') as fo:
                first = False
                for line in fo:
                    fea = line.rstrip('\n').split('\t')
                    feature_index[fea[0]] = max_index
                    max_index += 1
            if is_flag_true == True:
                os.remove(feature_index_file)
        return max_index,feature_index,first

    def get_name_col (self, train_raw):
        nameCol = {}
        with open(train_raw, 'r') as file:
            for line in file:
                s = line.split('\t')
                for i in range(0,len(s)):
                    nameCol[s[i].strip()] = i
        return nameCol

    def process_data_onehot(self, train_raw, namecol, feature_index_file, first):
        random.seed(1000)
        with open(train_raw, 'r') as fi:
            is_flag_train = True
            max_index,feature_index,first = self.load_feature_from_old_file(feature_index_file, first, is_flag_train)
            for line in fi:
                data_element = line.strip().split('\t')
                if first:   #obtain the original feature name
                    first = False
                    for i in range(0, len(data_element)):
                        namecol[data_element[i]] = i
                        if i > 0:
                            feature_index[data_element[i].strip() + '@other'] = max_index
                            max_index += 1
                    continue
                if data_element[0].isalpha():
                    continue
                for f in self.__f1s:
                    try:
                        col = namecol[f]
                        content = data_element[col] # s[]: original feature name list
                        if random.randint(1,1000) != 10:
                            feat = f + '@' + content
                        else:
                            feat = f + '@other'
                        if feat not in feature_index:
                            feature_index[feat] = max_index
                            max_index += 1
                    except IndexError:
                        pass
                for f in self.__f1sp:
                    col = namecol[f]
                    content = self.feature_trainsform(f, data_element[col])
                    if random.randint(1,1000) != 10:
                        feat = f + '@' + content
                    else:
                        feat = f + '@other'
                    if feat not in feature_index:
                        feature_index[feat] = max_index
                        max_index += 1
                self.show_progress(process_name= 'MG data')
        return namecol, feature_index, max_index

    def save_feature_index(self, max_index, feature_index, feature_index_file):
        print 'feature size: {0}'.format(max_index)
        feature_index = sorted(feature_index.iteritems(), key=operator.itemgetter(1))
        with open(feature_index_file, 'w') as fo:
            for fv in feature_index:
                fo.write(fv[0] + '\t' + str(fv[1]) + '\n')

    def save_onehot_data_to_file(self, raw_data, vw_data, namecol, feature_index):
        with open(raw_data, 'r') as fi:
            with open(vw_data, 'w') as fo:
                first = True
                for line in fi:
                    if first:
                        first = False
                        continue
                    data_element = line.split('\t')
                    if int(data_element[0]) == 0:
                        fo.write('-1'+' | ')
                    else:
                        fo.write('1'+' | ')
                    for f in self.__f1s: # every direct first order feature
                        try:
                            col = namecol[f]
                            content = data_element[col]
                            feat = f + '@' + content
                            if feat not in feature_index:
                                feat = f + '@other'
                            fo.write(' ' + feat + ":1")
                        except IndexError:
                            pass
                    for f in self.__f1sp:
                        col = namecol[f]
                        content = self.feature_trainsform(f, data_element[col])
                        feat = f + '@' + content
                        if feat not in feature_index:
                            feat = f + '@other'
                        fo.write(' ' + feat + ":1")
                    # col = namecol["usertag"]
                    # tags = get_tags(s[col])
                    # for tag in tags:
                    #     feat = str(col) + ':' + tag
                    #     if feat not in feature_index:
                    #         feat = str(col) + ':other'
                    #     index = feature_index[feat]
                    #     fo.write(' ' + str(index) + ":1")
                    fo.write('\n')

    def one_hot_train_set(self, train_raw, train_vw, feature_index_file):
        namecol = self.get_name_col(train_raw)
        first = True
        namecol, feature_index, max_index = self.process_data_onehot(train_raw, namecol, feature_index_file, first)
        self.reset_counter()
        self.save_feature_index(max_index, feature_index, feature_index_file)
        self.save_onehot_data_to_file(train_raw, train_vw, namecol, feature_index)
        feature_index.clear()

    def one_hot_test_set(self, test_raw, test_vw, feature_index_file):
        namecol = self.get_name_col(test_raw)
        first = True
        is_flag_train = False
        max_index,feature_index,first = self.load_feature_from_old_file(feature_index_file,first, is_flag_train)
        self.save_onehot_data_to_file(test_raw, test_vw, namecol, feature_index)
        feature_index.clear()
