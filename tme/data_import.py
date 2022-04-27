import numpy as np


def import_front_data(fileName):
    f = open(fileName, 'r')
    lines = f.readlines()
    index = 0
    num_f = int(len(lines) / 26)
    data = np.zeros((num_f + 1, 25, 4))
    for line in lines:
        line = line.split(',')[0]
        number = index % 25
        value_x = float(line[0])
        value_y = float(line[1])
        value_z = float(line[2])
        confidence = float(line[3])
        data[index, number, :] = [value_x, value_y, value_z, confidence]
    return data


def import_back_data(fileName):
    trans_map = [0, 1, 2, 3, 8, 9, 10, 11, 4, 5, 6, 7, 16, 17,
                 18, 19, 12, 13, 14, 15, 20, 23, 24, 21, 22]
    f = open(fileName, 'r')
    lines = f.readlines()
    index = 0
    num_f = int(len(lines) / 26)
    data = np.zeros((num_f + 1, 25, 4))
    for line in lines:
        line = line.split(',')[0]
        number = index % 25
        value_x = float(line[0])
        value_y = float(line[1])
        value_z = float(line[2])
        confidence = float(line[3])
        data[index, trans_map[number], :] = [value_x, value_y, value_z, confidence]
    return data

