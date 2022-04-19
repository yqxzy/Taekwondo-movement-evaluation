
# frame: 0
# 0,-0.560858,0.285851,2.47564
# 1,-0.535059,0.615428,2.44133
# 2,-0.508015,0.933042,2.39516
# 3,-0.576195,1.07308,2.4352
# 4,-0.690399,0.822588,2.52275
# 5,-0.832548,0.919179,2.41502
# 6,-0.675953,0.816322,2.48645
# 7,-0.681044,0.799631,2.47892
# 8,-0.447853,0.758333,2.28621
# 9,-0.559638,0.578535,2.2063
# 10,-0.74439,0.550314,2.13055
# 11,-0.806921,0.541885,2.10903
# 12,-0.604144,0.289603,2.47729
# 13,-0.668668,-0.033478,2.35085
# 14,-0.727896,-0.341972,2.24641
# 15,-0.789536,-0.385857,2.13779
# 16,-0.502713,0.274521,2.40236
# 17,-0.485587,-0.0528475,2.48995
# 18,-0.480765,-0.3492,2.46667
# 19,-0.522593,-0.429356,2.43522
# 20,-0.515082,0.855356,2.4088
# 21,-0.684782,0.769095,2.47784
# 22,-0.685547,0.766194,2.4685
# 23,-0.815942,0.536731,2.12813
# 24,-0.800655,0.523096,2.10099
# the data is like ↑, 这是其中的一帧，0-18代表19个骨架, xyz就是它们的三维坐标
# 原始数据是紊乱的，所以要滤波处理
import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv



class skeleton_nodes:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.x = []
        self.y = []
        self.z = []


class skeleton_list:
    def __init__(self):
        self.sk = {0: skeleton_nodes('SpineBase', 0), 1: skeleton_nodes('SpineMid', 1), 2: skeleton_nodes('Neck', 2),
                   3: skeleton_nodes('Head', 3), 4: skeleton_nodes('ShoulderLeft', 4),
                   5: skeleton_nodes('ElbowLeft', 5), 6: skeleton_nodes('WristLeft', 6),
                   7: skeleton_nodes('HandLeft', 7), 8: skeleton_nodes('ShoulderSpine', 8),
                   9: skeleton_nodes('ElbowRight', 9), 10: skeleton_nodes('WristRight', 10),
                   11: skeleton_nodes('HandRight', 11), 12: skeleton_nodes('HipLeft', 12),
                   13: skeleton_nodes('KneeLeft', 13), 14: skeleton_nodes('AnkleLeft', 14),
                   15: skeleton_nodes('FootLeft', 15), 16: skeleton_nodes('HipRight', 16),
                   17: skeleton_nodes('KneeRight', 17), 18: skeleton_nodes('AnkleRight', 18),
                   19: skeleton_nodes('FootRight', 19), 20: skeleton_nodes('SpineShouder', 20),
                   21: skeleton_nodes('HandTipLeft', 21), 22: skeleton_nodes('ThumbLeft', 22),
                   23: skeleton_nodes('HandTipRight', 23), 24: skeleton_nodes('ThumbRight', 24)}


# 数据
def import_data(fileName, sk):
    f = open(fileName, 'r')
    lines = f.readlines()
    flag = 0
    index = -1
    for line in lines:
        if 'frame: ' in line:
            index = index + 1
            flag = 1
            continue
        if flag == 1:
            line = line.split('\n')[0]
            number = int(line.split(',')[0])
            value_x = line.split(',')[1]
            value_y = line.split(',')[2]
            value_z = line.split(',')[3]
            sk[number].x.append(float(value_x))
            sk[number].y.append(float(value_y))
            sk[number].z.append(float(value_z))
            if number == 24:
                flag = 0
    return index


def mean_filtering(list, row):
    w = 4
    start = round(w / 2)
    b = start - 1

    list_ = list[0:row - 1]

    for j in range(row - b - start):
        for i in range(b):
            list[start + j] = list[start + j] + list[start + j - i] + list[start + j + i]
        list[start + j] = list[start + j] / w

    list = list[0:row - 1]

    t = pd.read_csv(filepath_or_buffer='tests.csv', header=0, names=['fsp', 'coordinate'],
                    dtype={'fsp': np.int, 'coordinate': np.float})

    save = pd.DataFrame({'fsp': t['fsp'].values, 'coordinate': list})
    save.to_csv('smooth_' + 'tests.csv')

    plt.plot((t['fsp'].values).tolist(), list_, label='original data')
    plt.plot((t['fsp'].values).tolist(), list, label='smoothed data')
    plt.legend()
    plt.show()
    return list


def median_filtering(list, row):
    w = 5
    start = round(w / 2)
    b = start - 1

    list_ = list[0:row - 1]
    for j in range(row - b - start):
        A = list[j:j + w - 1]
        A = sorted(A)
        list[j + start - 1] = A[start]
    list = list[0:row - 1]

    t = pd.read_csv(filepath_or_buffer='tests.csv', header=0, names=['fsp', 'coordinate'],
                    dtype={'fsp': np.int, 'coordinate': np.float})

    save = pd.DataFrame({'fsp': t['fsp'].values, 'coordinate': list})
    save.to_csv('smooth_' + 'tests.csv')

    plt.plot((t['fsp'].values).tolist(), list_, label='original data')
    plt.plot((t['fsp'].values).tolist(), list, label='smoothed data')
    plt.legend()
    plt.show()

    return list


def write(num):
    f = open('tests.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(f)
    for i in range(num):
        csv_writer.writerow([i, 0.0])
    f.close()


# 标准




# process

def angle(a, b, c, i):
    x1, y1, z1 = (a.x[i] - b.x[i]), (a.y[i] - b.y[i]), (a.z[i] - b.z[i])  # 向量1
    x2, y2, z2 = (c.x[i] - b.x[i]), (c.y[i] - b.y[i]), (c.z[i] - b.z[i])  # 向量2

    cos_b = (x1 * x2 + y1 * y2 + z1 * z2) / (
            math.sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2) * (math.sqrt(x2 ** 2 + y2 ** 2 + z2 ** 2)))

    # cos(1,2)
    B = math.degrees(math.acos(cos_b))
    return B


def get_angle_list(sk):
    angle_list = np.ones((len(sk[0].x), 9))
    for i in range(len(sk[0].x)):
        angle_list[i][0] = angle(sk[6], sk[5], sk[4], i)
        angle_list[i][1] = angle(sk[5], sk[4], sk[20], i)
        angle_list[i][2] = angle(sk[20], sk[8], sk[9], i)
        angle_list[i][3] = angle(sk[8], sk[9], sk[10], i)
        angle_list[i][4] = angle(sk[0], sk[12], sk[13], i)
        angle_list[i][5] = angle(sk[12], sk[13], sk[14], i)
        angle_list[i][6] = angle(sk[0], sk[16], sk[17], i)
        angle_list[i][7] = angle(sk[16], sk[17], sk[18], i)
        angle_list[i][8] = angle(sk[20], sk[1], sk[0], i)
    return angle_list

class Action:
    def __init__(self,angle_list):
        self.alist=angle_list



# 判断是否有动作缺失或顺序错误，并将动作分割
def divide(sd, sk,w, Y, l,):
    # sd :标准动作集合
    # sk :用户动作集合
    # w :每个角度的权重
    # Y :判断动作是否存在的阈值
    # l :正偏移量
    s_list = get_angle_list(sd)
    u_list = get_angle_list(sk)
    d={}
    d_min=1e7
    static_list={}
    dynamic_list={}
    f_s={}
    f_e={}
    end=0
    for i in range(len(s_list)):
        for j in range(len(u_list)):
            d[j]=(s_list[i][0]-u_list[j][0])**2*w[0]+(s_list[i][1]-u_list[j][1])**2*w[1]+(s_list[i][2]-u_list[j][2])**2*w[2]\
                  +(s_list[i][3]-u_list[j][3])**2*w[3]+(s_list[i][4]-u_list[j][4])**2*w[4]+(s_list[i][5]-u_list[j][5])**2*w[5]\
                  +(s_list[i][6]-u_list[j][6])**2*w[6]+(s_list[i][7]-u_list[j][7])**2*w[7]+(s_list[i][8]-u_list[j][8])**2*w[8]
            if d[j] < d_min:
                d_min=d[j]
        if d_min > Y:
            print("动作缺失")
            return False

        j_s=1e7
        j_e=-1e7
        for j in range(len(d)):
            if d[j] <= d_min + l:
                if j>j_e:
                    j_e=j
                if j<j_s:
                    j_s=j

        static_list[i] = Action(u_list[j_s:j_e])
        dynamic_list[i]=Action(u_list[end:j_s])
        end=j_e
        f_s[i] = j_s
        f_e[i] = j_e
    return static_list,dynamic_list,f_s,f_e

def compare(sta_s,sta_d,s_list, d_list):
    s_dis=[]
    d_dis=[]
    for i in range(sta_s):
        s_dis.append(static_compare(sta_s[i], s_list[i].alist))
    for i in range(sta_d):
        d_dis.append(dynamic_compare(sta_d[i], d_list[i].alist))

    return s_dis, d_dis

def static_compare(B, E):
    d = np.ones((9, 1))
    for k in range(len(E[0])):
        sum=0
        for i in range(len(E)):
            sum += E[i][k]

        d[k] = sum/(len(E))-B[k]
    return d


def dynamic_compare(B, E):
    d = np.ones((9, 1))
    for k in range(len(E[0])):
        D = np.ones((len(E), len(B)))
        G = np.ones((len(E), len(B)))
        for i in range(len(E)):
            for j in range(len(B)):
                D[i][j] = (E[i][k] - B[j][k]) ** 2

        for i in range(len(E)):
            for j in range(len(B)):
                if i > 0 and j > 0:
                    G[i][j] = D[i][j] + min(D[i][j - 1], D[i - 1][j], D[i - 1][j - 1])
                elif i > 0:
                    G[i][j] = D[i][j] + D[i - 1][j]
                elif j > 0:
                    G[i][j] = D[i][j] + D[i][j - 1]
                else:
                    G[i][j] = D[i][j]

        d[k] = G[len(E) - 1][len(B) - 1] / (len(B) + len(E))
    return d



# 动作持续时间
def continue_time(f_s, f_e,fps=30):
    t_s = []
    t_d = []

    for i in range(len(f_s)):
        t_s[i] = (f_e[i] - f_s[i]) / fps

    t_d[0]=f_s[0]
    for i in range(len(f_s) - 1):
        t_d[i+1] = (f_s[i + 1] - f_e[i]) / fps

    return t_s,t_d


# 动态动作平均角速度比较
def mean_palstance_compare(E, B, fps=30):
    w = []
    e = []
    for i in range(len(B[0])):
        w[i] = 0
        for j in range(len(B) - 1):
            w[i] += fps*(B[j+1][i] - B[j][i])
        w[i] = w[i]/(len(B) - 1)

    for i in range(len(E[0])):
        e[i] = 0
        for j in range(len(E) - 1):
            e[i] += fps*(E[j+1][i] - E[j][i])
        e[i] = e[i]/(len(E) - 1) - w[i]

    return e

if __name__ == '__main__':
    s_user = skeleton_list()
    fp = import_data('./Teakwondo_3d_actions/test2.txt', s_user.sk)
    p = 0
    write(fp)
    s_key =skeleton_list()
    fp2 = import_data('./Teakwondo_3d_actions/pictureNode0.txt', s_key.sk)
    w=[1,1,1,1,1,1,1,1,1]
    print(s_key.sk[0].x)
    static_list,dynamic_list,f_s,f_e=divide(s_key.sk,s_user.sk,w,100,10)
    print(f_s)
    print(f_e)

