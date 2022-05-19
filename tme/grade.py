import math

import pandas as pd
from partition import compute_difference
from data_process import get_angle


def score(data):
    grade = {}
    frame = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
             19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
    grade["action1"] = score_act1(frame[0:3], data, 0)
    grade["action2"] = score_act2(frame[3:5], data, 0)
    grade["action3"] = score_act3(frame[5:6], data, 0)
    grade["action4"] = score_act4(frame[6:8], data, 0)
    grade["action5"] = score_act5(frame[8:10], data, 0)
    grade["action6"] = score_act6(frame[10:12], data, 0)
    grade["action7"] = score_act7(frame[12:13], data, 0)
    grade["action8"] = score_act8(frame[13:15], data, 0)
    grade["action9"] = score_act9(frame[15:17], data, 0)
    grade["action10"] = score_act10(frame[17:19], data, 0)
    grade["action11"] = score_act11(frame[19:20], data, 0)
    grade["action12"] = score_act12(frame[20:22], data, 0)
    grade["action13"] = score_act13(frame[22:23], data, 0)
    grade["action14"] = score_act14(frame[23:25], data, 0)
    grade["action15"] = score_act15(frame[25:29], data, 0)
    grade["action16"] = score_act16(frame[29:31], data, 0)
    grade["action17"] = score_act17(frame[31:35], data, 0)
    grade["action18"] = score_act18(frame[35:37], data, 0)
    grade["action19"] = score_act19(frame[37:38], data, 0)
    grade["action20"] = score_act20(frame[38:], data, 0)

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
    left_hand_angle = get_angle(data[frame[1], 20, :], data[frame[1], 8, :], data[frame[1], 9, :])
    if left_hand_angle > 140 or left_hand_angle < 90:
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
    right_hand_angle = get_angle(data[frame[1], 20, :], data[frame[1], 4, :], data[frame[1], 5, :])
    if right_hand_angle > 140 or right_hand_angle < 90:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)
    return score_list


def score_act5(frame, data, angle_list):
    score_list = []

    # 1. 冲拳, 左脚立起
    # Left-hand on left waist
    waist_x, waist_y = data[frame[0], 8, 0], (data[frame[0], 0, 1] + data[frame[0], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[0], 11, 0] - waist_x) > 0.05 or abs(data[frame[0], 11, 1] - waist_y) > 0.1:
        m = - 0.1
    # Right-hand punch
    if abs(data[frame[0], 7, 0] - data[frame[0], 1, 0]) > 0.1 or abs(
            data[frame[0], 7, 1] - data[frame[0], 1, 1]) > 0.1:
        m -= 0.1
    # Left-heel lift
    if data[frame[0], 18, 1] - data[frame[0], 19, 1] <= 0:
        m -= 0.1
    score_list.append(m)

    # 2. 反手冲拳, 左脚向前一步
    # Right-hand on right waist
    waist_x, waist_y = data[frame[1], 4, 0], (data[frame[1], 0, 1] + data[frame[1], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[1], 7, 0] - waist_x) > 0.05 or abs(data[frame[1], 7, 1] - waist_y) > 0.1:
        m = - 0.1
    # Left-hand punch
    if abs(data[frame[1], 11, 1] - data[frame[1], 1, 1]) > 0.1 or abs(
            data[frame[1], 11, 0] - data[frame[1], 1, 0]) > 0.1:
        m -= 0.1
    # Feet distance (Left feet in front)
    feet_distance = abs(data[frame[1], 19, 0] - data[frame[1], 15, 0])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act6(frame, data, angle_list):
    score_list = []

    # 1. 脚不变，右手(左)腰部，左手(右)肩部
    wrist_x, wrist_y = data[frame[0], 8, 0], (data[frame[0], 0, 0] + data[frame[0], 1, 0]) / 2 - 0.05
    m = 0
    # Left-hand on right-shoulder
    if compute_difference(data[frame[0], 11, :], data[frame[0], 4, :]) > 0.1:
        m = -0.1
    # Right-hand on left-waist
    if abs(data[frame[0], 7, 0] - wrist_x) > 0.05 or abs(data[frame[0], 7, 1] - wrist_y) > 0.1:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 右手(右)腰部, 左手角度, 两脚隔一个脚长
    # Right-hand on right-waist
    wrist_x, wrist_y = data[frame[1], 4, 0], (data[frame[1], 0, 0] + data[frame[1], 1, 0]) / 2 - 0.05
    m = 0
    if abs(data[frame[1], 7, 0] - wrist_x) > 0.05 or abs(data[frame[1], 7, 1] - wrist_y) > 0.1:
        m = -0.1
    # Feet distance (Left feet in front)
    feet_distance = abs(data[frame[1], 19, 2] - data[frame[1], 15, 2])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    # Left-hand angle
    left_hand_angle = get_angle(data[frame[1], 20, :], data[frame[1], 8, :], data[frame[1], 9, :])
    if left_hand_angle > 140 or left_hand_angle < 90:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act7(frame, data, angle_list):
    score_list = []

    # 2. 腿不变，反手冲拳，左脚向前一步
    # Left-hand on left-waist
    waist_x, waist_y = data[frame[0], 8, 2], (data[frame[0], 0, 1] + data[frame[0], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[0], 11, 2] - waist_x) > 0.05 or abs(data[frame[0], 11, 1] - waist_y) > 0.1:
        m = - 0.1
    # Right-hand punch
    if abs(data[frame[0], 7, 1] - data[frame[0], 1, 1]) > 0.1 or abs(
            data[frame[0], 7, 2] - data[frame[0], 1, 2]) > 0.1:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act8(frame, data, angle_list):
    score_list = []

    # 1. 右拳, 脚不变，左臂角度
    # Right-hand punch
    if abs(data[frame[0], 7, 0] - data[frame[0], 1, 0]) > 0.1 or abs(
            data[frame[0], 7, 1] - data[frame[0], 1, 1]) > 0.1:
        m = -0.1
    # Left-hand angle
    left_hand_angle = get_angle(data[frame[0], 20, :], data[frame[0], 8, :], data[frame[0], 9, :])
    if left_hand_angle > 200 or left_hand_angle < 160:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 右手(右)腰部，左拳角度，右脚向前一步
    # Right-hand on right waist
    waist_x, waist_y = data[frame[1], 4, 0], (data[frame[1], 0, 1] + data[frame[1], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[1], 7, 0] - waist_x) > 0.05 or abs(data[frame[1], 7, 1] - waist_y) > 0.1:
        m = - 0.1
    # Feet distance (Right feet in front)
    feet_distance = abs(data[frame[1], 15, 0] - data[frame[1], 19, 0])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    # Left-hand angle
    left_hand_angle = get_angle(data[frame[1], 20, :], data[frame[1], 8, :], data[frame[1], 9, :])
    if left_hand_angle > 140 or left_hand_angle < 90:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act9(frame, data, angle_list):
    score_list = []

    # 1. 左拳，左脚立起，右脚向前一步
    # Right-hand on right waist
    waist_x, waist_y = data[frame[0], 4, 0], (data[frame[0], 0, 1] + data[frame[0], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[0], 7, 0] - waist_x) > 0.05 or abs(data[frame[0], 7, 1] - waist_y) > 0.1:
        m = - 0.1
    # Left-hand punch
    if abs(data[frame[0], 11, 0] - data[frame[0], 1, 0]) > 0.1 or abs(
            data[frame[0], 11, 1] - data[frame[0], 1, 1]) > 0.1:
        m -= 0.1
    # Left-heel lift
    if data[frame[0], 18, 1] - data[frame[0], 19, 1] <= 0:
        m -= 0.1
    # Feet distance (Right feet in front)
    feet_distance = abs(data[frame[1], 15, 0] - data[frame[1], 19, 0])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 右拳，左手(左)腰部，左脚向前一步
    # Left-hand on left waist
    waist_x, waist_y = data[frame[1], 8, 0], (data[frame[1], 0, 1] + data[frame[1], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[1], 11, 0] - waist_x) > 0.05 or abs(data[frame[1], 11, 1] - waist_y) > 0.1:
        m = - 0.1
    # Right-hand punch
    if abs(data[frame[1], 7, 1] - data[frame[1], 1, 1]) > 0.1 or abs(
            data[frame[1], 7, 0] - data[frame[1], 1, 0]) > 0.1:
        m -= 0.1
    # Feet distance (Left feet in front)
    feet_distance = abs(data[frame[1], 19, 0] - data[frame[1], 15, 0])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act10(frame, data, angle_list):
    score_list = []

    # 1. 左拳, 右手角度，左脚立起
    # Left-hand punch
    if abs(data[frame[0], 11, 0] - data[frame[0], 1, 0]) > 0.1 or abs(
            data[frame[0], 11, 1] - data[frame[0], 1, 1]) > 0.1:
        m = -0.1
    # Left-heel lift
    if data[frame[0], 18, 1] - data[frame[0], 19, 1] <= 0:
        m -= 0.1
    # Right-hand angle
    right_hand_angle = get_angle(data[frame[0], 20, :], data[frame[0], 4, :], data[frame[0], 5, :])
    if right_hand_angle > 200 or right_hand_angle < 160:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 左手(左)腰部，右拳角度，左脚向前一步
    # Left-hand on left waist
    waist_x, waist_y = data[frame[1], 8, 0], (data[frame[1], 0, 1] + data[frame[1], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[1], 11, 0] - waist_x) > 0.05 or abs(data[frame[1], 11, 1] - waist_y) > 0.1:
        m = - 0.1
    # Feet distance (Left feet in front)
    feet_distance = abs(data[frame[1], 19, 0] - data[frame[1], 15, 0])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    # Right-hand angle
    right_hand_angle = get_angle(data[frame[1], 20, :], data[frame[1], 4, :], data[frame[1], 5, :])
    if right_hand_angle > 140 or right_hand_angle < 90:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act11(frame, data, angle_list):
    score_list = []

    # 1. 左反手冲拳, 右脚向前一步
    # Right-hand on right waist
    waist_x, waist_y = data[frame[0], 4, 0], (data[frame[0], 0, 1] + data[frame[0], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[0], 7, 0] - waist_x) > 0.05 or abs(data[frame[0], 7, 1] - waist_y) > 0.1:
        m = - 0.1
    # Left-hand punch
    if abs(data[frame[0], 11, 1] - data[frame[0], 1, 1]) > 0.1 or abs(
            data[frame[0], 11, 0] - data[frame[0], 1, 0]) > 0.1:
        m -= 0.1
    # Feet distance (Right feet in front)
    feet_distance = abs(data[frame[0], 15, 0] - data[frame[0], 19, 0])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act12(frame, data, angle_list):
    score_list = []

    # 1. 右手(左)肩部，左手(右)腰部，右脚立起，左脚向前一步
    wrist_x, wrist_y = data[frame[0], 4, 0], (data[frame[0], 0, 0] + data[frame[0], 1, 0]) / 2 - 0.05
    m = 0
    # Right-hand on left-shoulder
    if compute_difference(data[frame[0], 7, :], data[frame[0], 8, :]) > 0.1:
        m = -0.1
    # Left-hand on right-waist
    if abs(data[frame[0], 11, 0] - wrist_x) > 0.05 or abs(data[frame[0], 11, 1] - wrist_y) > 0.1:
        m -= 0.1
    # Right-heel lift
    if data[frame[0], 14, 1] - data[frame[0], 15, 1] <= 0:
        m -= 0.1
    # Feet distance (Left feet in front)
    feet_distance = abs(data[frame[1], 19, 0] - data[frame[1], 15, 0])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 左手(左)腰部, 右手角度, 两脚隔一个脚长, 右腿弓步角度
    # Left-hand on left-waist
    wrist_x, wrist_y = data[frame[1], 8, 0], (data[frame[1], 0, 0] + data[frame[1], 1, 0]) / 2 - 0.05
    m = 0
    if abs(data[frame[1], 11, 0] - wrist_x) > 0.05 or abs(data[frame[1], 11, 1] - wrist_y) > 0.1:
        m = -0.1
    # Right-hand angle
    right_hand_angle = get_angle(data[frame[1], 20, :], data[frame[1], 4, :], data[frame[1], 5, :])
    if right_hand_angle > 140 or right_hand_angle < 90:
        m -= 0.1
    # Feet distance (Right feet in front)
    feet_distance = abs(data[frame[1], 15, 2] - data[frame[1], 19, 2])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    # Right-leg angle
    right_leg_angle = get_angle(data[frame[1], 12, :], data[frame[1], 13, :], data[frame[1], 14, :])
    if right_leg_angle > 120 or right_leg_angle < 80:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act13(frame, data, angle_list):
    score_list = []

    # 2. 腿不变，左反手冲拳
    # Right-hand on right-waist
    waist_x, waist_y = data[frame[0], 4, 2], (data[frame[0], 0, 1] + data[frame[0], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[0], 7, 2] - waist_x) > 0.05 or abs(data[frame[0], 7, 1] - waist_y) > 0.1:
        m = - 0.1
    # Left-hand punch
    if abs(data[frame[0], 11, 1] - data[frame[0], 1, 1]) > 0.1 or abs(
            data[frame[0], 11, 2] - data[frame[0], 1, 2]) > 0.1:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act14(frame, data, angle_list):
    score_list = []

    # 1. 脚不变，右手(左)肩部，左手(右)腰部
    wrist_x, wrist_y = data[frame[0], 4, 0], (data[frame[0], 0, 0] + data[frame[0], 1, 0]) / 2 - 0.05
    m = 0
    # Right-hand on left-shoulder
    if compute_difference(data[frame[0], 7, :], data[frame[0], 8, :]) > 0.1:
        m = -0.1
    # Left-hand on right-waist
    if abs(data[frame[0], 11, 0] - wrist_x) > 0.05 or abs(data[frame[0], 11, 1] - wrist_y) > 0.1:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 右手(右)腰部，左拳角度，左脚向前一步
    # Right-hand on right waist
    waist_x, waist_y = data[frame[1], 4, 0], (data[frame[1], 0, 1] + data[frame[1], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[1], 7, 0] - waist_x) > 0.05 or abs(data[frame[1], 7, 1] - waist_y) > 0.1:
        m = - 0.1
    # Feet distance (Left feet in front)
    feet_distance = abs(data[frame[1], 19, 0] - data[frame[1], 15, 0])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    # Left-hand angle
    left_hand_angle = get_angle(data[frame[1], 20, :], data[frame[1], 8, :], data[frame[1], 9, :])
    if left_hand_angle > 280 or left_hand_angle < 220:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act15(frame, data, angle_list):
    score_list = []

    # 1. 双手在胸口到腰之间，右腿角度（上提），左腿角度（直）
    m = 0
    # Both hand between chest and waist
    waist_y = (data[frame[0], 0, 1] + data[frame[0], 1, 1]) / 2
    upper_waist_y = (data[frame[0], 0, 1] + waist_y) / 2 - 0.05
    if (abs(data[frame[0], 7, 1] - upper_waist_y)) > 0.1 or (
            abs(data[frame[0], 11, 1] - upper_waist_y) > 0.1):
        m = -0.1
    # Right-leg angle
    right_leg_angle = get_angle(data[frame[0], 12, :], data[frame[0], 13, :], data[frame[0], 14, :])
    if right_leg_angle > 100 or right_leg_angle < 60:
        m -= 0.1
    # Left-leg angle
    left_leg_angle = get_angle(data[frame[0], 16, :], data[frame[0], 17, :], data[frame[0], 18, :])
    if left_leg_angle > 190 or left_leg_angle < 170:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 双手不变，双腿角度(直)，右腿高于肩膀
    # Right feet higher than shoulder
    m = 0
    if data[frame[1], 15, 1] < data[frame[1], 4, 1]:
        m -= 0.1
    # Right-leg angle
    right_leg_angle = get_angle(data[frame[1], 0, :], data[frame[1], 12, :], data[frame[1], 13, :])
    if right_leg_angle > 190 or right_leg_angle < 170:
        m -= 0.1
    # Left-leg angle
    left_leg_angle = get_angle(data[frame[1], 16, :], data[frame[1], 17, :], data[frame[1], 18, :])
    if left_leg_angle > 190 or left_leg_angle < 170:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 3. 右手(右)腰部，左反手冲拳位置及角度，右腿角度（上提），左腿角度（直）
    # Right-hand on right-waist
    waist_x, waist_y = data[frame[2], 4, 0], (data[frame[2], 0, 1] + data[frame[2], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[2], 7, 0] - waist_x) > 0.05 or abs(data[frame[2], 7, 1] - waist_y) > 0.1:
        m = - 0.1
    # Left-hand punch
    if abs(data[frame[2], 11, 1] - data[frame[2], 1, 1]) > 0.1 or abs(
            data[frame[2], 11, 0] - data[frame[2], 1, 0]) > 0.1:
        m -= 0.1
    # Right-leg angle
    right_leg_angle = get_angle(data[frame[2], 12, :], data[frame[2], 13, :], data[frame[2], 14, :])
    if right_leg_angle > 100 or right_leg_angle < 60:
        m -= 0.1
    # Left-leg angle
    left_leg_angle = get_angle(data[frame[2], 16, :], data[frame[2], 17, :], data[frame[2], 18, :])
    if left_leg_angle > 190 or left_leg_angle < 170:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 4. 左手(左)腰部，右反手冲拳, 右脚向前一步
    # Left-hand on left-waist
    waist_x, waist_y = data[frame[3], 8, 0], (data[frame[3], 0, 1] + data[frame[3], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[3], 11, 0] - waist_x) > 0.05 or abs(data[frame[3], 11, 1] - waist_y) > 0.1:
        m = - 0.1
    # Right-hand punch
    if abs(data[frame[3], 7, 1] - data[frame[3], 1, 1]) > 0.1 or abs(
            data[frame[3], 7, 0] - data[frame[3], 1, 0]) > 0.1:
        m -= 0.1
    # Feet distance (Right feet in front)
    feet_distance = abs(data[frame[3], 15, 0] - data[frame[3], 19, 0])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act16(frame, data, angle_list):
    score_list = []

    # 1. 脚不变，左手(右)肩部，右手(左)腰部
    wrist_x, wrist_y = data[frame[0], 8, 0], (data[frame[0], 0, 0] + data[frame[0], 1, 0]) / 2 - 0.05
    m = 0
    # Left-hand on right-shoulder
    if compute_difference(data[frame[0], 11, :], data[frame[0], 4, :]) > 0.1:
        m = -0.1
    # Right-hand on left-waist
    if abs(data[frame[0], 7, 0] - wrist_x) > 0.05 or abs(data[frame[0], 7, 1] - wrist_y) > 0.1:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 左手(左)腰部，右拳角度，右脚向前一步
    # Left-hand on left waist
    waist_x, waist_y = data[frame[1], 8, 0], (data[frame[1], 0, 1] + data[frame[1], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[1], 11, 0] - waist_x) > 0.05 or abs(data[frame[1], 11, 1] - waist_y) > 0.1:
        m = - 0.1
    # Right-hand angle
    right_hand_angle = get_angle(data[frame[1], 20, :], data[frame[1], 4, :], data[frame[1], 5, :])
    if right_hand_angle > 270 or right_hand_angle < 220:
        m -= 0.1
    # Feet distance (Right feet in front)
    feet_distance = abs(data[frame[1], 15, 0] - data[frame[1], 19, 0])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act17(frame, data, angle_list):
    score_list = []

    # 1. 双手在胸口到腰之间，左腿角度（上提），右腿角度（直）
    m = 0
    # Both hand between chest and waist
    waist_y = (data[frame[0], 0, 1] + data[frame[0], 1, 1]) / 2
    upper_waist_y = (data[frame[0], 0, 1] + waist_y) / 2 - 0.05
    if (abs(data[frame[0], 7, 1] - upper_waist_y)) > 0.1 or (
            abs(data[frame[0], 11, 1] - upper_waist_y) > 0.1):
        m = -0.1
    # Right-leg angle
    right_leg_angle = get_angle(data[frame[0], 12, :], data[frame[0], 13, :], data[frame[0], 14, :])
    if right_leg_angle > 190 or right_leg_angle < 170:
        m -= 0.1
    # Left-leg angle
    left_leg_angle = get_angle(data[frame[0], 16, :], data[frame[0], 17, :], data[frame[0], 18, :])
    if left_leg_angle > 100 or left_leg_angle < 60:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 双手不变，双腿角度(直)，左腿高于肩膀
    # Left feet higher than shoulder
    m = 0
    if data[frame[1], 19, 1] < data[frame[1], 8, 1]:
        m -= 0.1
    # Right-leg angle
    right_leg_angle = get_angle(data[frame[1], 12, :], data[frame[1], 13, :], data[frame[1], 14, :])
    if right_leg_angle > 190 or right_leg_angle < 170:
        m -= 0.1
    # Left-leg angle
    left_leg_angle = get_angle(data[frame[1], 0, :], data[frame[1], 16, :], data[frame[1], 17, :])
    if left_leg_angle > 190 or left_leg_angle < 170:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 3. 左手(左)腰部，右反手冲拳位置及角度，左腿角度（上提），右腿角度（直）
    # Left-hand on left-waist
    waist_x, waist_y = data[frame[2], 8, 0], (data[frame[2], 0, 1] + data[frame[2], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[2], 11, 0] - waist_x) > 0.05 or abs(data[frame[2], 11, 1] - waist_y) > 0.1:
        m = - 0.1
    # Right-hand punch
    if abs(data[frame[2], 7, 1] - data[frame[2], 1, 1]) > 0.1 or abs(
            data[frame[2], 7, 0] - data[frame[2], 1, 0]) > 0.1:
        m -= 0.1
    # Right-leg angle
    right_leg_angle = get_angle(data[frame[2], 12, :], data[frame[2], 13, :], data[frame[2], 14, :])
    if right_leg_angle > 190 or right_leg_angle < 170:
        m -= 0.1
    # Left-leg angle
    left_leg_angle = get_angle(data[frame[2], 16, :], data[frame[2], 17, :], data[frame[2], 18, :])
    if left_leg_angle > 100 or left_leg_angle < 60:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 4. 右手(右)腰部，左反手冲拳, 左脚向前一步
    # Right-hand on right-waist
    waist_x, waist_y = data[frame[3], 4, 0], (data[frame[3], 0, 1] + data[frame[3], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[3], 7, 0] - waist_x) > 0.05 or abs(data[frame[3], 7, 1] - waist_y) > 0.1:
        m = - 0.1
    # Left-hand punch
    if abs(data[frame[3], 11, 1] - data[frame[3], 1, 1]) > 0.1 or abs(
            data[frame[3], 11, 0] - data[frame[3], 1, 0]) > 0.1:
        m -= 0.1
    # Feet distance (Left feet in front)
    feet_distance = abs(data[frame[3], 19, 0] - data[frame[3], 15, 0])
    if feet_distance > 0.3 or feet_distance < 0.2:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act18(frame, data, angle_list):
    score_list = []

    # 1. 左手(右)肩部，右手(左)腰部
    wrist_x, wrist_y = data[frame[0], 8, 0], (data[frame[0], 0, 0] + data[frame[0], 1, 0]) / 2 - 0.05
    m = 0
    # Left-hand on right-shoulder
    if compute_difference(data[frame[0], 11, :], data[frame[0], 4, :]) > 0.1:
        m = -0.1
    # Right-hand on left-waist
    if abs(data[frame[0], 7, 0] - wrist_x) > 0.05 or abs(data[frame[0], 7, 1] - wrist_y) > 0.1:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 右手(右)腰部，左拳角度，双腿角度
    # Right-hand on right waist
    waist_x, waist_y = data[frame[1], 4, 0], (data[frame[1], 0, 1] + data[frame[1], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[1], 7, 0] - waist_x) > 0.05 or abs(data[frame[1], 7, 1] - waist_y) > 0.1:
        m = - 0.1
    # Left-hand angle
    left_hand_angle = get_angle(data[frame[1], 20, :], data[frame[1], 8, :], data[frame[1], 9, :])
    if left_hand_angle > 140 or left_hand_angle < 90:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act19(frame, data, angle_list):
    score_list = []

    # 1. 左手(左)腰部，右反手冲拳，双腿角度
    # Left-hand on left-waist
    waist_x, waist_y = data[frame[0], 8, 2], (data[frame[0], 0, 1] + data[frame[0], 1, 1]) / 2 - 0.05
    m = 0
    if abs(data[frame[0], 11, 2] - waist_x) > 0.05 or abs(data[frame[0], 11, 1] - waist_y) > 0.1:
        m = - 0.1
    # Right-hand punch
    if abs(data[frame[0], 7, 1] - data[frame[0], 1, 1]) > 0.1 or abs(
            data[frame[0], 7, 2] - data[frame[0], 1, 2]) > 0.1:
        m -= 0.1
    # Right-leg angle
    right_leg_angle = get_angle(data[frame[0], 12, :], data[frame[0], 13, :], data[frame[0], 14, :])
    if right_leg_angle > 120 or right_leg_angle < 80:
        m -= 0.1
    # Left-leg angle
    left_leg_angle = get_angle(data[frame[0], 16, :], data[frame[0], 17, :], data[frame[0], 18, :])
    if left_leg_angle > 190 or left_leg_angle < 170:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list


def score_act20(frame, data, angle_list):
    score_list = []

    # 1. 提至胸口握拳，拳心向上: 双手在胸口，肩膀角度，两脚距离
    m = 0
    if (abs(data[frame[0], 7, 1] - data[frame[0], 1, 1])) > 0.1 or (
            abs(data[frame[0], 11, 1] - data[frame[0], 1, 1]) > 0.1):
        m = -0.1
    if abs(data[frame[0], 15, 0] - data[frame[0], 19, 0]) < 0.3 or abs(
            data[frame[0], 15, 0] - data[frame[0], 19, 0]) > 0.5:
        m = m - 0.1
    # Right-shoulder angle
    right_shoulder_angle = get_angle(data[frame[0], 20, :], data[frame[0], 4, :], data[frame[0], 5, :])
    if right_shoulder_angle > 140 or right_shoulder_angle < 100:
        m -= 0.1
    # Left-shoulder angle
    left_shoulder_angle = get_angle(data[frame[0], 20, :], data[frame[0], 8, :], data[frame[0], 9, :])
    if left_shoulder_angle > 140 or left_shoulder_angle < 100:
        m -= 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    # 2. 双手小腹前，两拳之间一拳距离
    m = 0
    if (data[frame[1], 7, 1] > data[frame[1], 0, 1] + 0.2 or data[frame[1], 7, 1] < data[frame[1], 0, 1] + 0.1) or (
            data[frame[1], 11, 1] > data[frame[1], 1, 1] + 0.2 or data[frame[1], 11, 1] < data[frame[1], 1, 1] + 0.1):
        m = -0.1
    if abs(data[frame[1], 7, 0] - data[frame[1], 11, 0]) < 0.1 or abs(
            data[frame[1], 7, 0] - data[frame[1], 11, 0]) > 0.15:
        m = m - 0.1
    m = ('%.1f' % m)
    score_list.append(m)

    return score_list