__author__ = 'Jiahao Dong'

def process_vwformat(raw_data_path, train_set_vw):
    file_handle = open(raw_data_path, 'r')
    vw_data_file = open(train_set_vw, 'w')
    feature_name = file_handle.readline().rstrip('\n').split('\t')
    print  feature_name
    line = file_handle.readline()
    i = 0
    while line:
        attri_value = line.rstrip('\n').split('\t')
        if attri_value[0] == '0':
            new_example = '-1'
        else:
            new_example = '1'
        for i in range(1,len(attri_value),1):
            feature =  ' | ' + feature_name[i] + ':' + attri_value[i]
            new_example += feature
        vw_data_file.write(new_example + '\n')
        line = file_handle.readline()
        i += 1
        if i>20:
            break
