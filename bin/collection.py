import pygame
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import sys
import cv2
from matplotlib import pyplot as plt

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

# colors for drawing different bodies
SKELETON_COLORS = [pygame.color.THECOLORS["red"],
                   pygame.color.THECOLORS["blue"],
                   pygame.color.THECOLORS["green"],
                   pygame.color.THECOLORS["orange"],
                   pygame.color.THECOLORS["purple"],
                   pygame.color.THECOLORS["yellow"],
                   pygame.color.THECOLORS["violet"]]


class KinectRuntime(object):
    def __init__(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._done = False
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1),
                                               pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE, 32)
        pygame.display.set_caption("Kinect for Windows v2 Body Game")
        self._clock = pygame.time.Clock()
        self._kinect = PyKinectRuntime.PyKinectRuntime(
            PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Infrared | PyKinectV2.FrameSourceTypes_Body)
        self._frame_surface = pygame.Surface(
            (self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)
        self._bodies = None
        self._text_file = open('1.txt', mode='w')
        # self._fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
        # self._fps = 30
        # self._size = cv2.CAP_PROP_FRAME_WIDTH,cv2.CAP_PROP_FRAME_HEIGHT
        # self._outVideo = cv2.VideoWriter('saveDir.avi', self._fourcc, self._fps, self._size)
        self.file_num = 0
        self.pic_num = 0
        self.start = False

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

        if self.start:
            self._text_file.write(
                "%f,%f,%f,%d" % (
                joints[0].Position.x, joints[0].Position.y, joints[0].Position.z, joints[0].TrackingState))
            self._text_file.write(
                "%f,%f,%f,%d" % (
                joints[1].Position.x, joints[1].Position.y, joints[1].Position.z, joints[1].TrackingState))
            self._text_file.write(
                "%f,%f,%f,%d" % (
                joints[2].Position.x, joints[2].Position.y, joints[2].Position.z, joints[2].TrackingState))
            self._text_file.write(
                "%f,%f,%f,%d" % (
                joints[3].Position.x, joints[3].Position.y, joints[3].Position.z, joints[3].TrackingState))
            self._text_file.write(
                "%f,%f,%f,%d" % (
                joints[4].Position.x, joints[4].Position.y, joints[4].Position.z, joints[4].TrackingState))
            self._text_file.write(
                "%f,%f,%f,%d" % (
                joints[5].Position.x, joints[5].Position.y, joints[5].Position.z, joints[5].TrackingState))
            self._text_file.write(
                "%f,%f,%f,%d" % (
                joints[6].Position.x, joints[6].Position.y, joints[6].Position.z, joints[6].TrackingState))
            self._text_file.write(
                "%f,%f,%f,%d" % (
                joints[7].Position.x, joints[7].Position.y, joints[7].Position.z, joints[7].TrackingState))
            self._text_file.write(
                "%f,%f,%f,%d" % (
                joints[8].Position.x, joints[8].Position.y, joints[8].Position.z, joints[8].TrackingState))
            self._text_file.write(
                "%f,%f,%f,%d" % (
                joints[9].Position.x, joints[9].Position.y, joints[9].Position.z, joints[9].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[10].Position.x, joints[10].Position.y, joints[10].Position.z, joints[10].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[11].Position.x, joints[11].Position.y, joints[11].Position.z, joints[11].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[12].Position.x, joints[12].Position.y, joints[12].Position.z, joints[12].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[13].Position.x, joints[13].Position.y, joints[13].Position.z, joints[13].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[14].Position.x, joints[14].Position.y, joints[14].Position.z, joints[14].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[15].Position.x, joints[15].Position.y, joints[15].Position.z, joints[15].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[16].Position.x, joints[16].Position.y, joints[16].Position.z, joints[16].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[17].Position.x, joints[17].Position.y, joints[17].Position.z, joints[17].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[18].Position.x, joints[18].Position.y, joints[18].Position.z, joints[18].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[19].Position.x, joints[19].Position.y, joints[19].Position.z, joints[19].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[20].Position.x, joints[20].Position.y, joints[20].Position.z, joints[20].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[21].Position.x, joints[21].Position.y, joints[21].Position.z, joints[21].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[22].Position.x, joints[22].Position.y, joints[22].Position.z, joints[22].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[23].Position.x, joints[23].Position.y, joints[23].Position.z, joints[23].TrackingState))
            self._text_file.write("%f,%f,%f,%d" % (
                joints[24].Position.x, joints[24].Position.y, joints[24].Position.z, joints[24].TrackingState))

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
        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self._done = True  # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE:  # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'],
                                                           pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE, 32)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # 按回車開始
                        self.start = True
                    if event.key == pygame.K_SPACE:  # 按空格結束
                        self.start = False
                    if event.key == pygame.K_p:  # 按P拍照
                        fname = "pic_%d.png" % self.pic_num
                        pygame.image.save(self._screen, fname)
                        self.file_num = self.file_num + 1

            # --- Game logic should go here

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
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked:
                        continue

                    joints = body.joints
                    # convert joint coordinates to color space
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self.draw_body(joints, joint_points, SKELETON_COLORS[i])

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size)
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0, 0))
            surface_to_draw = None
            pygame.display.update()

            if self.start:
                fname = "Snaps_%d.png" % self.file_num
                pygame.image.save(self._screen, fname)
                self.file_num = self.file_num + 1

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self._text_file.close()
        self._kinect.close()
        pygame.quit()


__main__ = "Kinect v2 Body Game"
game = KinectRuntime();
game.run();
