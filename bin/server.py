import ctypes
import struct
import sys
import time
from socket import *

import cv2
import numpy
import pygame
from PIL import Image
from pykinect2 import PyKinectRuntime
from pykinect2 import PyKinectV2

if sys.hexversion >= 0x03000000:
    pass
else:
    pass

# colors for drawing different bodies
SKELETON_COLORS = [pygame.color.THECOLORS["red"],
                   pygame.color.THECOLORS["blue"],
                   pygame.color.THECOLORS["green"],
                   pygame.color.THECOLORS["orange"],
                   pygame.color.THECOLORS["purple"],
                   pygame.color.THECOLORS["yellow"],
                   pygame.color.THECOLORS["violet"]]


class KinectServer(object):
    def __init__(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._done = False
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1),
                                               pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE, 32)
        pygame.display.set_caption("Taekwondo-movement-evaluation")
        self._clock = pygame.time.Clock()
        self._kinect = PyKinectRuntime.PyKinectRuntime(
            PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Infrared | PyKinectV2.FrameSourceTypes_Body)
        self._frame_surface = pygame.Surface(
            (self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)
        self._bodies = None
        self._text_file_1 = None
        self._text_file_2 = None
        self.file_num = 0
        self.pic_num = 0
        self.start = False
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('', 1111))
        self.sock.listen(5)
        self.pic = False
        self.bone_file_2 = None
        self.bone_file_1 = None
        self.data = "".encode()
        self.conn = None
        self.addr = None
        self.video = None

    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked):
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except:  # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):
        # save position
        payload_size = struct.calcsize("Q")
        self.data = b''
        while len(self.data) < payload_size:
            self.data += self.conn.recv(1024)
        print(len(self.data))
        packed_size = self.data[:payload_size]
        self.data = self.data[payload_size:]
        msg_size = struct.unpack("Q", packed_size)[0]
        print(msg_size)

        # while len(self.data) < msg_size:
        #     self.data += self.conn.recv(1024)
        zframe_data = self.data[:msg_size]
        self.data = zframe_data
        # print(self.data)

        data_1 = ""
        if self.start:
            self._text_file_2.write(self.data.decode())

            for i in range(25):
                data_1 += (
                        "%f,%f,%f,%d\n" % (
                    joints[i].Position.x, joints[i].Position.y, joints[i].Position.z, joints[i].TrackingState))

            self._text_file_1.write(data_1)

        if self.pic:
            for i in range(25):
                data_1 += (
                        "%f,%f,%f,%d\n" % (
                    joints[i].Position.x, joints[i].Position.y, joints[i].Position.z, joints[i].TrackingState))

            self.bone_file_1.write(data_1)
            self.bone_file_2.write(self.data.decode())
            self.bone_file_1.close()
            self.bone_file_2.close()
            self.pic = False
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder,
                            PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder,
                            PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder,
                            PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);

        # Right Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight,
                            PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight,
                            PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight,
                            PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight,
                            PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight,
                            PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft,
                            PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft,
                            PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight,
                            PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight,
                            PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);

    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    def run(self):
        while True:
            print('Waiting...')
            try:
                self.conn, self.addr = self.sock.accept()
                print('Client connected:', self.addr)
            except KeyboardInterrupt:
                print('Server shutdown')
                break
            except Exception as e:
                print(e)
                continue
            # -------- Main Program Loop -----------
            while not self._done:
                # --- Game logic should go here
                # --- Main event loop
                for event in pygame.event.get():  # User did something
                    if event.type == pygame.QUIT:  # If user clicked close
                        self._done = True  # Flag that we are done so we exit this loop

                    elif event.type == pygame.VIDEORESIZE:  # window resized
                        self._screen = pygame.display.set_mode(event.dict['size'],
                                                               pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE,
                                                               32)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # 按回車開始
                            print("Start!")
                            self.start = True
                            self.file_num += 1
                            self._text_file_1 = open(str(self.file_num) + '_1.txt', mode='w')
                            self._text_file_2 = open(str(self.file_num) + '_2.txt', mode='w')
                            fps = 30
                            size = self._screen.get_size()
                            file_path = str(int(time.time())) + ".avi"  # 导出路径
                            fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
                            self.video = cv2.VideoWriter(file_path, fourcc, fps, size)
                        if event.key == pygame.K_SPACE:  # 按空格結束
                            print("Stop!")
                            self.start = False
                            self._text_file_1.close()
                            self._text_file_2.close()
                            self.video.release()
                        if event.key == pygame.K_p:  # 按P拍照
                            pic_name = "pic_%d.png" % self.pic_num
                            bone_1 = "Snaps/pic_%d_1.txt" % self.pic_num
                            bone_2 = "Snaps/pic_%d_2.txt" % self.pic_num
                            pygame.image.save(self._screen, pic_name)
                            self.bone_file_1 = open(bone_1, mode='w')
                            self.bone_file_2 = open(bone_2, mode='w')
                            self.pic_num = self.pic_num + 1
                            self.pic = True
                # --- Getting frames and drawing
                # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data
                if self._kinect.has_new_color_frame():
                    frame = self._kinect.get_last_color_frame()
                    self.draw_color_frame(frame, self._frame_surface)
                    frame = None

                # --- Cool! We have a body frame, so can get skeletons
                if self._kinect.has_new_body_frame():
                    self._bodies = self._kinect.get_last_body_frame()

                # --- draw skeletons to _frame_surface
                if self._bodies is not None:
                    # for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[0]
                    if not body.is_tracked:
                        continue

                    joints = body.joints
                    # convert joint coordinates to color space
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self.draw_body(joints, joint_points, SKELETON_COLORS[0])

                # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
                # --- (screen size may be different from Kinect's color frame size)
                h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
                target_height = int(h_to_w * self._screen.get_width())
                surface_to_draw = pygame.transform.scale(self._frame_surface,
                                                         (self._screen.get_width(), target_height));
                self._screen.blit(surface_to_draw, (0, 0))
                surface_to_draw = None
                pygame.display.update()

                if self.start:
                    imagestring = pygame.image.tostring(
                        self._screen.subsurface(0, 0, self._screen.get_width(), self._screen.get_height()), "RGB")
                    pilImage = Image.frombytes("RGB", self._screen.get_size(), imagestring)
                    img = cv2.cvtColor(numpy.asarray(pilImage), cv2.COLOR_RGB2BGR)

                    self.video.write(img)  # 把图片写进视频

                # --- Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

                # --- Limit to 60 frames per second
                self._clock.tick(60)

            # Close our Kinect sensor, close the window and quit.
            self._kinect.close()
            self.sock.close()
            pygame.quit()


__main__ = "TME"

game = KinectServer();
game.run();
