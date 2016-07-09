__author__ = 'Jiahao Dong'

def randomize_dataset(file_read_path, file_write_path, max_rounds, max_mod):
    for i in range(0,max_rounds,1):
        print 'round {}'.format(i)
        with open(file_write_path, 'w') as writefile:
            for modNo in range(0,max_mod,1):
                with open(file_read_path, 'r') as readfile:
                    print 'finish reading data from file to list'
                    count = 0
                    for line in readfile:
                        if count%max_mod == modNo:
                            writefile.write(line)
                        count += 1

if __name__ == "__main__":
    origin_set_path = '../../make-ipinyou-data/all/'
    origin_file_path = '{0}train.log.txt'.format(origin_set_path)
    new_file_path = '{0}train.txt'.format(origin_set_path)
    max_rounds = 10
    max_mod = 100
    randomize_dataset(origin_file_path, new_file_path, max_rounds, max_mod)