import numpy as np


def import_front_data(fileName):
    f = open(fileName, 'r')
    lines = f.readlines()
    index = 0
    frame=-1
    num_f = int(len(lines) / 25)
    data = np.zeros((num_f, 25, 4))
    for line in lines:
        line = line.split(',')
        number = index % 25
        if number == 0: frame+=1
        value_x = float(line[0])
        value_y = float(line[1])
        value_z = float(line[2])
        line[3]=line[3].replace('\n','')
        confidence = int(line[3])
        data[frame, number, :] = [value_x, value_y, value_z, confidence]
        index+=1
        # print(data[index, number, :])

    return data


def import_back_data(fileName):
    trans_map = [0, 1, 2, 3, 8, 9, 10, 11, 4, 5, 6, 7, 16, 17,
                 18, 19, 12, 13, 14, 15, 20, 23, 24, 21, 22]
    f = open(fileName, 'r')
    lines = f.readlines()
    index = 0
    frame = -1
    num_f = int(len(lines) / 25)
    data = np.zeros((num_f , 25, 4))
    for line in lines:
        line = line.split(',')
        number = index % 25
        if number == 0: frame += 1
        value_x = float(line[0])
        value_y = float(line[1])
        value_z = float(line[2])
        line[3] = line[3].replace('\n', '')
        confidence = int(line[3])
        data[frame, trans_map[number], :] = [value_x, value_y, value_z, confidence]
        index+=1
    return data

