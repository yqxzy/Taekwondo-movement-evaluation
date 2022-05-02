import numpy as np
import math


def Bursa(data_C, data_D):
    point = [0, 1, 5, 9, 13, 17]
    L = []
    B = np.empty((0, 7))
    for i in range(len(point)):
        # 提取元素
        X_C = data_C[0, i, 0]
        Y_C = data_C[0, i, 1]
        Z_C = data_C[0, i, 2]
        X_D = data_D[0, i, 0]
        Y_D = data_D[0, i, 1]
        Z_D = data_D[0, i, 2]

        L.extend((X_C - X_D, Y_C - Y_D, Z_C - Z_D))

        b1 = np.array([1, 0, 0, 0, -Z_D, Y_D, X_D])
        b2 = np.array([0, 1, 0, Z_D, 0, -X_D, Y_D])
        b3 = np.array([0, 0, 1, -Y_D, X_D, 0, Z_D])
        BB = np.row_stack((b1, b2, b3))
        B = np.append(B, BB, axis=0)
    B = B
    L = np.array([L]).T

    a = np.linalg.inv(np.dot(B.T, B))
    b = np.dot(B.T, L)
    x = np.dot(a, b)

    return x


def trans_data(data_C, data_D):
    x = Bursa(data_C, data_D)
    data_d = np.zeros((len(data_D), 25, 4))
    for i in range(len(data_D)):
        # 提取元素
        for k in range(25):
            XN_D = data_D[i, k, 0]
            YN_D = data_D[i, k, 1]
            ZN_D = data_D[i, k, 2]
            LN = np.row_stack((XN_D, YN_D, ZN_D))

            bn1 = np.array([1, 0, 0, 0, -ZN_D, YN_D, XN_D])
            bn2 = np.array([0, 1, 0, ZN_D, 0, -XN_D, YN_D])
            bn3 = np.array([0, 0, 1, -YN_D, XN_D, 0, ZN_D])
            BN = np.row_stack((bn1, bn2, bn3))
            NCC = np.dot(BN, x) + LN
            data_d[i, k, 0] = NCC[0][0]
            data_d[i, k, 1] = NCC[1][0]
            data_d[i, k, 2] = NCC[2][0]
            data_d[i, k, 3] = data_D[i, k, 3]
    return data_d


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
