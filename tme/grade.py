import math

import pandas as pd
from partition import compute_difference


def score(data):
    grade = {}
    frame = [0, 1, 2, 3, 4, 5, 6, 7]
    grade["action1"] = score_act1(frame[0:3], data, 0)
    grade["action2"] = score_act2(frame[3:5], data, 0)
    grade["action3"] = score_act3(frame[5:6], data, 0)
    grade["action4"] = score_act4(frame[6:], data, 0)

    return grade


def score_act1(frame, data, angle_list):
    score_list = []

    # 1.立正姿势: 双脚并拢
    if abs(data[frame[0], 15, 0] - data[frame[0], 19, 0]) > 0.15:
        score_list.append(-0.1)
    else:
        score_list.append(0)

    # 2. 提至胸口握拳，拳心向上: 双手在胸口，肩膀角度，两脚距离
    m = 0
    if (abs(data[frame[1], 7, 1] - data[frame[1], 1, 1])) > 0.1 or (
            abs(data[frame[1], 11, 1] - data[frame[1], 1, 1]) > 0.1):
        m = -0.1
    if abs(data[frame[1], 15, 0] - data[frame[1], 19, 0]) < 0.3 or abs(
            data[frame[1], 15, 0] - data[frame[1], 19, 0]) > 0.5:
        m = m - 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 3. 双手小腹前，两拳之间一拳距离
    m = 0
    if (data[frame[2], 7, 1] > data[frame[2], 0, 1] + 0.2 or data[frame[2], 7, 1] < data[frame[2], 0, 1] + 0.1) or (
            data[frame[2], 11, 1] > data[frame[2], 1, 1] + 0.2 or data[frame[2], 11, 1] < data[frame[2], 1, 1] + 0.1):
        m = -0.1
    if abs(data[frame[2], 7, 0] - data[frame[2], 11, 0]) < 0.1 or abs(
            data[frame[2], 7, 0] - data[frame[2], 11, 0]) > 0.15:
        m = m - 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act2(frame, data, angle_list):
    score_list = []

    # 1.左手肩部，右手腰部
    wrist_x, wrist_y = data[frame[0], 8, 0], (data[frame[0], 0, 0] + data[frame[0], 1, 0]) / 2 - 0.05
    m = 0
    if compute_difference(data[frame[0], 11, :], data[frame[0], 4, :]) > 0.1:
        m = -0.1
    if abs(data[frame[0], 7, 0] - wrist_x) > 0.05 or abs(data[frame[0], 7, 1] - wrist_y) > 0.1:
        m = m - 0.1
    m = ('%.1f' % m)

    score_list.append(m)

    # 2. 右手(右)腰部, 左手角度, 两脚隔一个脚长
    wrist_x, wrist_y = data[frame[1], 4, 0], (data[frame[1], 0, 0] + data[frame[1], 1, 0]) / 2 - 0.05
    m = 0
    if abs(data[frame[1], 7, 0] - wrist_x) > 0.05 or abs(data[frame[1], 7, 1] - wrist_y) > 0.1:
        m = - 0.1
    if data[frame[1], 19, 0] - data[frame[1], 15, 0] > 0.3 or data[frame[1], 19, 0] - data[frame[1], 15, 0] < 0.2:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act3(frame, data, angle_list):
    score_list = []

    # 1. 反手冲拳, 右脚向前一步
    waist_x, waist_y = data[frame[0], 8, 0], (data[frame[0], 0, 1] + data[frame[0], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[0], 11, 0] - waist_x) > 0.05 or abs(data[frame[0], 11, 1] - waist_y) > 0.1:
        m = - 0.1
    if abs(data[frame[0], 7, 1] - data[frame[0], 1, 1]) > 0.1 or abs(
            data[frame[0], 7, 0] - data[frame[0], 1, 0]) > 0.1:
        m -= 0.1
    if data[frame[0], 15, 0] - data[frame[0], 19, 0] > 0.3 or data[frame[0], 15, 0] - data[frame[0], 19, 0] < 0.2:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act4(frame, data, angle_list):
    score_list = []

    # 1. 脚不变，手
    wrist_x, wrist_y = data[frame[0], 4, 0], (data[frame[0], 0, 0] + data[frame[0], 1, 0]) / 2 - 0.05
    m = 0
    if compute_difference(data[frame[0], 7, :], data[frame[0], 8, :]) > 0.1:
        m = -0.1
    if abs(data[frame[0], 11, 0] - wrist_x) > 0.05 or abs(data[frame[0], 11, 1] - wrist_y) > 0.1:
        m = m - 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 左手(右)腰部, 右手角度, 两脚隔一个脚长
    wrist_x, wrist_y = data[frame[1], 8, 0], (data[frame[1], 0, 0] + data[frame[1], 1, 0]) / 2 - 0.05
    m = 0
    if abs(data[frame[1], 11, 0] - wrist_x) > 0.05 or abs(data[frame[1], 11, 1] - wrist_y) > 0.1:
        m = - 0.1
    if data[frame[1], 15, 0] - data[frame[1], 15, 0] > 0.3 or data[frame[1], 19, 0] - data[frame[1], 15, 0] < 0.2:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)
    return score_list
