__author__ = 'Jiahao Dong'

def get_original_label (file_read_path, file_write_path):
    with open(file_read_path, 'r') as readfile:
        with open(file_write_path, 'w') as writefile:
            for line in readfile:
                parts = line.rstrip('\n').split(' | ')
                if int(parts[0]) == 1:
                    writefile.write('1\n')
                else:
                    writefile.write('-1\n')
