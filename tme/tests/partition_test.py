import numpy as np
import matplotlib.pyplot as plt
import cv2

from tme.data_import import *
from tme.data_process import *



def Print3D(num_frame, point, arms, legs, body):
    # 求坐标最大值
    xmax = np.max(point[:, :, 0])
    xmin = np.min(point[:, :, 0])
    ymax = np.max(point[:, :, 1])
    ymin = np.min(point[:, :, 1])
    zmax = np.max(point[:, :, 2])
    zmin = np.min(point[:, :, 2])

    plt.figure()
    plt.ion()

    for i in range(num_frame):
        plt.cla()

        plot3D = plt.subplot(projection='3d')
        plot3D.view_init(120, -90)

        Expan_Multiple = 1.4

        plot3D.scatter(point[i, :20, 0] * Expan_Multiple, point[i, :20, 1] * Expan_Multiple, point[i, :20, 2],
                       c='red', s=40.0)

        plot3D.plot(point[i, arms, 0] * Expan_Multiple, point[i, arms, 1] * Expan_Multiple, point[i, arms, 2],
                    c='green', lw=2.0)
        # plot3D.plot(point[i, rightHand, 0] * Expan_Multiple, point[i, rightHand, 1] * Expan_Multiple,
        #             point[i, rightHand, 2], c='green', lw=2.0)
        # plot3D.plot(point[i, leftHand, 0] * Expan_Multiple, point[i, leftHand, 1] * Expan_Multiple,
        #             point[i, leftHand, 2], c='green', lw=2.0)
        plot3D.plot(point[i, legs, 0] * Expan_Multiple, point[i, legs, 1] * Expan_Multiple, point[i, legs, 2],
                    c='green', lw=2.0)
        plot3D.plot(point[i, body, 0] * Expan_Multiple, point[i, body, 1] * Expan_Multiple, point[i, body, 2],
                    c='green', lw=2.0)

        plot3D.text(xmax - 0.3, ymax + 1.1, zmax + 0.3, 'frame: {}/{}'.format(i, num_frame - 1))
        plot3D.set_xlim3d(xmin - 0.5, xmax + 0.5)
        plot3D.set_ylim3d(ymin - 0.3, ymax + 0.3)
        plot3D.set_zlim3d(zmin - 0.3, zmax + 0.3)
        plt.savefig('/Users/wangzeyu/Taekwondo-movement-evaluation/data/test/partition/pic-{}.png'.format(i + 1))
        plt.pause(0.001)

    plt.ioff()
    plt.show()


if __name__ == '__main__':
    data_f = import_front_data('/Users/wangzeyu/Taekwondo-movement-evaluation/data/test/score/wzy/pic_front.txt')
    data_back = import_back_data('/Users/wangzeyu/Taekwondo-movement-evaluation/data/test/score/wzy/pic_back.txt')
    data_b = trans_data(data_f, data_back)
    data = fuse_data(data_f, data_b)
    num_frame = len(data)

    arms = [ 11, 10, 9, 8, 20, 4, 5, 6, 7]
    # rightHand = [11, 24]
    # leftHand = [7, 22]
    legs = [19, 18, 17, 16, 0, 12, 13, 14, 15]
    body = [3, 2, 20, 1, 0]

    print(data)
    Print3D(num_frame, data, arms,  legs, body)

    # fps = 30
    # img_size = (640, 480)
    # i = 0

    # fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    # video_dir = './data/test/partition/video.mp4'
    # videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)
    #
    # for i in range(1, num_frame+1):
    #     for j in range(5):
    #         img_path = './data/test/partition/pic-{}.png'.format(i)
    #         frame = cv2.imread(img_path)
    #         frame = cv2.resize(frame, img_size)
    #         videoWriter.write(frame)
    #
    # videoWriter.release()
