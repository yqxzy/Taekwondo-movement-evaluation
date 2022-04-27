import numpy as np
import math


def rate_date():
    return


def fuse_data(data1, data2):
    data = np.zeros((len(data1), 25, 4))
    for i in range(len(data1)):
        for j in range(25):
            if data1[i, j, 3] > data2[i, j, 3]:
                for k in range(4):
                    data[i, j, k] = data1[i, j, k]
            else:
                for k in range(4):
                    data[i, j, k] = data2[i, j, k]
    return data


def mean_filtering(data):
    row = len(data)
    data_ = np.zeros((row, 25, 4))
    w = 4
    start = round(w / 2)
    b = start - 1

    for i in range(row - b - start):
        for j in range(25):
            for k in range(3):
                for m in range(b):
                    data_[start + i, j, k] = data_[start + i, j, k] + data_[start + i - m, j, k] + data_[
                        start + i + m, j, k]
                data_[start + i, j, k] = data_[start + i, j, k] / w

    return data_


def get_angle(point1, point2, point3):
    x1, y1, z1 = (point1[0] - point2[0]), (point1[1] - point2[1]), (point1[2] - point2[2])  # 向量1
    x2, y2, z2 = (point2[0] - point3[0]), (point2[1] - point3[1]), (point2[2] - point3[2])  # 向量2
    cos_b = (x1 * x2 + y1 * y2 + z1 * z2) / (
            math.sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2) * (math.sqrt(x2 ** 2 + y2 ** 2 + z2 ** 2)))
    angle = math.degrees(math.acos(cos_b))
    return angle


def get_angle_list(data):
    angle_list = np.zeros((len(data), 9, 1))
    for i in range(len(data)):
        angle_list[i, 0, :] = get_angle(data[i, 6, :], data[i, 5, :], data[i, 4, :])
        angle_list[i, 1, :] = get_angle(data[i, 5, :], data[i, 4, :], data[i, 20, :])
        angle_list[i, 2, :] = get_angle(data[i, 20, :], data[i, 8, :], data[i, 9, :])
        angle_list[i, 3, :] = get_angle(data[i, 8, :], data[i, 9, :], data[i, 10, :])
        angle_list[i, 4, :] = get_angle(data[i, 0, :], data[i, 12, :], data[i, 13, :])
        angle_list[i, 5, :] = get_angle(data[i, 12, :], data[i, 13, :], data[i, 14, :])
        angle_list[i, 6, :] = get_angle(data[i, 0, :], data[i, 16, :], data[i, 17, :])
        angle_list[i, 7, :] = get_angle(data[i, 16, :], data[i, 17, :], data[i, 18, :])
        angle_list[i, 8, :] = get_angle(data[i, 20, :], data[i, 1, :], data[i, 0, :])
    return angle_list
