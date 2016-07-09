__author__ = 'Jiahao Dong'

from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_curve_single(x, y, advertiser, result_path, train_rounds, graph_name):
    plt.figure()
    plt.ylabel(graph_name)
    plt.xlabel('rounds')
    plt.title(advertiser)
    plt.axis([0,train_rounds, min(y), max(y)])
    plt.setp(plt.plot(x,y), color='b' , linewidth = 1)
    plt.grid()
    # ax = plt.axes([0,train_rounds, min(y), max(y)])
    # ax.xaxis.set_major_locator(plt.MultipleLocator(1.0))
    # ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))
    # ax.yaxis.set_major_locator(plt.MultipleLocator(1.0))
    # ax.yaxis.set_minor_locator(plt.MultipleLocator(0.1))
    # plt.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='0.75')
    # plt.grid(which='minor', axis='x', linewidth=0.25, linestyle='-', color='0.75')
    # plt.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='0.75')
    # plt.grid(which='minor', axis='y', linewidth=0.25, linestyle='-', color='0.75')
    plt.savefig('{0}advertiser{1}_{2}.jpg'.format(result_path, advertiser, graph_name), dpi = 400)
    plt.close()

def plot_curve_all(x, y, test_file_name, result_path, counter):
    for i in range(0,len(test_file_name),1):
        label_name = str(test_file_name[i])
        plt.plot(x,y[i],label=label_name,linewidth=1)
    plt.xlabel('rounds')
    plt.ylabel('AUC')
    plt.legend(loc = 'upper left', borderpad = 1,prop={'size':6})
    plt.ylim(0.4,0.9)
    plt.grid()
    path = result_path + 'figure/'
    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)
    plt.savefig('{0}Curvefigure{1}.jpg'.format(path, counter), dpi = 400)
    plt.close()

def plot_bar(x, y, test_file_name, result_path, counter):
    opacity = 0.8
    plt.subplots()
    rect = plt.bar(np.arange(len(test_file_name)),y, align = 'center', alpha = opacity, color = 'r')
    plt.xlabel('Campaigns')
    plt.ylabel('AUC value')
    plt.xticks(np.arange(len(test_file_name)),test_file_name)
    for i in rect:
        height = i.get_height()
        plt.text(i.get_x(), 1.01*height, '%.3f' % float(height))
    plt.legend()
    plt.grid()
    path = '{0}figure/'.format(result_path)
    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)
    plt.savefig('{0}figure{1}.jpg'.format(path, counter))
    plt.close()

def get_predlabel(label_path, prediction_path):
    labels = []
    predictions = []
    with open(label_path, 'r') as label_file:
        for line in label_file:
            labels.append((float(line.rstrip('\n'))+1.0)/2)
    with open(prediction_path, 'r') as prediction_file:
        for line in prediction_file:
            predictions.append(float(line.rstrip('\n')))
    return labels, predictions

def calc_rmse(label_path, prediction_path):
    label, prediction = get_predlabel(label_path, prediction_path)
    return (mean_squared_error(label, prediction))**0.5

def calc_auc(label_path, prediction_path):
    label, prediction = get_predlabel(label_path, prediction_path)
    return roc_auc_score(label, prediction)

def calc_auc_list(label_path, prediction_path, test_file_name):
    y_auc = []
    for i in range(0,len(test_file_name),1):
        y_auc.append(calc_auc(label_path[i],prediction_path[i]))
    return y_auc

def set_rmse_axis_single_set(label_path, prediction_path, train_rounds):
    x_num = []
    y_rmse = []
    for i in range(0, train_rounds,1):
        x_num.append(i)
        y_rmse.append(calc_rmse(label_path, prediction_path[i]))
    for i in range(0, train_rounds):
        print 'RMSE: {0}'.format(y_rmse[i])
    return x_num, y_rmse

def set_auc_axis_single_set(label_path, prediction_path, train_rounds):
    x_num = []
    y_auc = []
    for i in range(0, train_rounds,1):
        x_num.append(i)
        y_auc.append(calc_auc(label_path, prediction_path[i]))
    for i in range(0, train_rounds):
        print 'AUC: {0}'.format(y_auc[i])
    return x_num, y_auc

def set_axis_multi_set(label_path, prediction_path, advertiser):
    x_num = []
    y_auc = []
    for i in range(0,len(advertiser),1):
        x_num.append(advertiser[i])
        y_auc.append(calc_auc(label_path[i],prediction_path[i]))
    return x_num, y_auc

def record_auc_to_file(auc_list, auc_file):
    with open(auc_file, 'w') as file:
        for val in auc_list:
            file.write('{}\n'.format(val))

# label_path:filePath, prediction_path:filePath array, train_rounds:int
def auc_graph(label_path, prediction_path, result_path, advertiser, train_rounds, chart, auc_file):
    if chart == 'curve_single':
        graph_name = 'AUC'
        x_num, y_auc = set_auc_axis_single_set(label_path, prediction_path, train_rounds)
        plot_curve_single(x_num, y_auc, advertiser, result_path, train_rounds, graph_name)
        graph_name = 'RMSE'
        x_num, y_rmse = set_rmse_axis_single_set(label_path, prediction_path, train_rounds)
        plot_curve_single(x_num, y_rmse, advertiser, result_path, train_rounds, graph_name)
        record_auc_to_file(y_auc, auc_file)
    elif chart == 'curve_all':
        x_num, y_auc = set_axis_multi_set(label_path, prediction_path, advertiser)
        plot_curve_all(x_num, y_auc, advertiser, result_path, train_rounds)
        record_auc_to_file(y_auc, auc_file)
    elif chart == 'bar':
        x_num, y_auc = set_axis_multi_set(label_path, prediction_path, advertiser)
        plot_bar(x_num, y_auc, advertiser, result_path, train_rounds)
        record_auc_to_file(y_auc, auc_file)