__author__ = 'Jiahao Dong'
import redis

def write_to_database(model_file_path):
    connection = redis.StrictRedis(db=1)
    with open(model_file_path) as file:
        for line in file:
            if line.strip().startswith('Constant'):
                parts = line.strip().split(':')
                connection.set(parts[0], float(parts[2]))
                break
        for line in file:
            parts = line.strip().split(':')
            connection.set(parts[0], float(parts[2]))
    print 'Stored {0} keys'.format(len(connection.keys()))

# model_file_path -> readable model file