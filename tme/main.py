from data_import import *
from data_process import *
from grade import *

if __name__ == '__main__':
    data_f = import_front_data('/Users/wangzeyu/Taekwondo-movement-evaluation/data/test/score/mcq/pic_front.txt')
    data_back = import_back_data('/Users/wangzeyu/Taekwondo-movement-evaluation/data/test/score/mcq/pic_back.txt')
    # print(data_f)
    # print(data_back)
    data_b = trans_data(data_f, data_back)
    # print(data_b)
    data = fuse_data(data_f, data_b)
    # print(data)
    score_list = score(data)
    print(score_list)
