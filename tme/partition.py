import numpy as np

# 标准动作数组
key_num = 9
w = np.ones(key_num)


def compute_difference(data1, data2):
    l = len(data1)
    for i in range(l):
        dif = dif + (data1[i, 0] - data2[i, 0]) ** 2 * w[i]
    return dif


def divide(key_data, data):
    frames = np.zeros(key_num)
    for i in range(key_num):
        min = 1e7
        for j in range(len(data)):
            dif = compute_difference(key_data[i, :, :], data[j, :, :])
            if i != 0:
                dif = dif + (j - frames[i - 1]) ** 2
            if dif < min:
                frames[i] = j
                min = dif
    return frames
