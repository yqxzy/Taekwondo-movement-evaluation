//  运行环境：
//      Windows11/10
//      Microsoft Visual Studio Community 2019 版本 16.10.2
//      opencv3.416
//      Kinect2.0_1409
#define _WINSOCK_DEPRECATED_NO_WARNINGS 
#include <stdio.h>
#include <stdlib.h>
#include<cstring>
#include<WS2tcpip.h>
#include <WinSock2.h>
#pragma comment(lib, "ws2_32.lib")  //加载 ws2_32.dll
#include<iostream>
#include<opencv2/calib3d.hpp>//opencv头文件
#include<opencv2/opencv.hpp>
#include<opencv2/core/core.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>
#include<Kinect.h>//kinect头文件
#include<conio.h>
#include<string>
#include<fstream>
#include<Windows.h>


using   namespace   std;
using   namespace   cv;


void    draw(Mat& img, Joint& r_1, Joint& r_2, ICoordinateMapper* myMapper);
int main(void)
{
    IKinectSensor* mySensor = nullptr;
    GetDefaultKinectSensor(&mySensor);
    //获取传感器

    mySensor->Open();
    //打开传感器

    IColorFrameSource* myColorSource = nullptr;
    mySensor->get_ColorFrameSource(&myColorSource);

    IColorFrameReader* myColorReader = nullptr;
    myColorSource->OpenReader(&myColorReader);
    //打开色彩数据阅读器

    int colorHeight = 0, colorWidth = 0;
    IFrameDescription* myDescription = nullptr;
    myColorSource->get_FrameDescription(&myDescription);
    myDescription->get_Height(&colorHeight);
    myDescription->get_Width(&colorWidth);
    myDescription->Release();
    myDescription = nullptr;
    //get info

    IColorFrame* myColorFrame = nullptr;
    Mat original(colorHeight, colorWidth, CV_8UC4);

    cv::Size frameSize(static_cast<int>(colorWidth), static_cast<int>(colorHeight));

    //*************************************以上为ColorFrame的读取做准备**************************************

    IBodyFrameSource* myBodySource = nullptr;
    mySensor->get_BodyFrameSource(&myBodySource);

    IBodyFrameReader* myBodyReader = nullptr;
    myBodySource->OpenReader(&myBodyReader);

    int myBodyCount = 0;
    myBodySource->get_BodyCount(&myBodyCount);

    IBodyFrame* myBodyFrame = nullptr;

    ICoordinateMapper* myMapper = nullptr;
    mySensor->get_CoordinateMapper(&myMapper);

    //*************************************以上为BodyFrame的读取以及Mapper做准备**************************************

    /*
    VideoWriter outputVideo("output0.mp4", CV_FOURCC('D', 'I', 'V', 'X'), 30.0, frameSize, 1);
    //创建视频文件
    if (!outputVideo.isOpened()) {
        cout << "fail to open the videowriter" << endl;
        system("pause");
        return -1;
    }

    ofstream ofs;
    //创建骨架节点坐标文件
    ofs.open("test0.txt", ios::out);
    */

    //*************************************以上为存储数据集做准备**************************************


    int frame = 0;
    int fileCount = 0;
    int pictureCount = 0;
    bool pictureFlag = 0;
    bool startFlag = 1;//初始状态为录制中

    //*************************************以下是socket传输部分**************************************
    cout << "-----------客户端-----------" << endl;

    //	1	初始化
    WSADATA wsadata;
    WSAStartup(MAKEWORD(2, 2), &wsadata);

    //	2	创建套接字
    SOCKET clientSocket = {};
    clientSocket = socket(PF_INET, SOCK_STREAM, 0);
    if (SOCKET_ERROR == clientSocket) {
        cout << "套接字闯创建失败!" << endl;
    }
    else {
        cout << "套接字创建成功!" << endl;
    }

    //	3	绑定套接字	指定绑定的IP地址和端口号
    sockaddr_in socketAddr;
    socketAddr.sin_family = PF_INET;
    socketAddr.sin_addr.S_un.S_addr = inet_addr("10.24.81.213");
    socketAddr.sin_port = htons(1234);
    int cRes = connect(clientSocket, (SOCKADDR*)&socketAddr, sizeof(SOCKADDR));

    if (SOCKET_ERROR == cRes) {
        cout << "客户端:\t\t与服务器连接失败....." << endl;
    }
    else {
        cout << "客户端:\t\t与服务器连接成功....." << endl;
    }

    while (1)
    {
        while (myColorReader->AcquireLatestFrame(&myColorFrame) != S_OK);
        myColorFrame->CopyConvertedFrameDataToArray(colorHeight * colorWidth * 4, original.data, ColorImageFormat_Bgra);
        Mat copy = original.clone();//读取彩色图像并输出到矩阵
        while (myBodyReader->AcquireLatestFrame(&myBodyFrame) != S_OK);
        //读取身体图像
        IBody** myBodyArr = new IBody * [myBodyCount];
        for (int i = 0; i < myBodyCount; i++)
            myBodyArr[i] = nullptr;

        frame = frame + 1;
        if (myBodyFrame->GetAndRefreshBodyData(myBodyCount, myBodyArr) == S_OK) //把身体数据输入数组
            for (int i = 0; i < myBodyCount; i++)

            {
                BOOLEAN     result = false;
                if (myBodyArr[i]->get_IsTracked(&result) == S_OK && result) //先判断是否侦测到
                {
                    Joint   myJointArr[JointType_Count];

                    if (myBodyArr[i]->GetJoints(JointType_Count, myJointArr) == S_OK) //如果侦测到就把关节数据输入到数组并画图 
                    {
                        if (startFlag)//把骨架坐标传给server(如果录制中，就写入骨架坐标)
                        {
                            //	4	发送请求
                            string s;
                            s = "frame: " + to_string(frame) + "\n";
                            s += "0," + to_string(myJointArr[0].Position.X) + "," + to_string(myJointArr[0].Position.Y) + "," + to_string(myJointArr[0].Position.Z) + "\n";
                            s += "1," + to_string(myJointArr[1].Position.X) + "," + to_string(myJointArr[1].Position.Y) + "," + to_string(myJointArr[1].Position.Z) + "\n";
                            s += "2," + to_string(myJointArr[2].Position.X) + "," + to_string(myJointArr[2].Position.Y) + "," + to_string(myJointArr[2].Position.Z) + "\n";
                            s += "3," + to_string(myJointArr[3].Position.X) + "," + to_string(myJointArr[3].Position.Y) + "," + to_string(myJointArr[3].Position.Z) + "\n";
                            s += "4," + to_string(myJointArr[4].Position.X) + "," + to_string(myJointArr[4].Position.Y) + "," + to_string(myJointArr[4].Position.Z) + "\n";
                            s += "5," + to_string(myJointArr[5].Position.X) + "," + to_string(myJointArr[5].Position.Y) + "," + to_string(myJointArr[5].Position.Z) + "\n";
                            s += "6," + to_string(myJointArr[6].Position.X) + "," + to_string(myJointArr[6].Position.Y) + "," + to_string(myJointArr[6].Position.Z) + "\n";
                            s += "7," + to_string(myJointArr[7].Position.X) + "," + to_string(myJointArr[7].Position.Y) + "," + to_string(myJointArr[7].Position.Z) + "\n";
                            s += "8," + to_string(myJointArr[8].Position.X) + "," + to_string(myJointArr[8].Position.Y) + "," + to_string(myJointArr[8].Position.Z) + "\n";
                            s += "9," + to_string(myJointArr[9].Position.X) + "," + to_string(myJointArr[9].Position.Y) + "," + to_string(myJointArr[9].Position.Z) + "\n";
                            s += "10," + to_string(myJointArr[10].Position.X) + "," + to_string(myJointArr[10].Position.Y) + "," + to_string(myJointArr[10].Position.Z) + "\n";
                            s += "11," + to_string(myJointArr[11].Position.X) + "," + to_string(myJointArr[11].Position.Y) + "," + to_string(myJointArr[11].Position.Z) + "\n";
                            s += "12," + to_string(myJointArr[12].Position.X) + "," + to_string(myJointArr[12].Position.Y) + "," + to_string(myJointArr[12].Position.Z) + "\n";
                            s += "13," + to_string(myJointArr[13].Position.X) + "," + to_string(myJointArr[13].Position.Y) + "," + to_string(myJointArr[13].Position.Z) + "\n";
                            s += "14," + to_string(myJointArr[14].Position.X) + "," + to_string(myJointArr[14].Position.Y) + "," + to_string(myJointArr[14].Position.Z) + "\n";
                            s += "15," + to_string(myJointArr[15].Position.X) + "," + to_string(myJointArr[15].Position.Y) + "," + to_string(myJointArr[15].Position.Z) + "\n";
                            s += "16," + to_string(myJointArr[16].Position.X) + "," + to_string(myJointArr[16].Position.Y) + "," + to_string(myJointArr[16].Position.Z) + "\n";
                            s += "17," + to_string(myJointArr[17].Position.X) + "," + to_string(myJointArr[17].Position.Y) + "," + to_string(myJointArr[17].Position.Z) + "\n";
                            s += "18," + to_string(myJointArr[18].Position.X) + "," + to_string(myJointArr[18].Position.Y) + "," + to_string(myJointArr[18].Position.Z) + "\n";
                            s += "19," + to_string(myJointArr[19].Position.X) + "," + to_string(myJointArr[19].Position.Y) + "," + to_string(myJointArr[19].Position.Z) + "\n";
                            s += "20," + to_string(myJointArr[20].Position.X) + "," + to_string(myJointArr[20].Position.Y) + "," + to_string(myJointArr[20].Position.Z) + "\n";
                            s += "21," + to_string(myJointArr[21].Position.X) + "," + to_string(myJointArr[21].Position.Y) + "," + to_string(myJointArr[21].Position.Z) + "\n";
                            s += "22," + to_string(myJointArr[22].Position.X) + "," + to_string(myJointArr[22].Position.Y) + "," + to_string(myJointArr[22].Position.Z) + "\n";
                            s += "23," + to_string(myJointArr[23].Position.X) + "," + to_string(myJointArr[23].Position.Y) + "," + to_string(myJointArr[23].Position.Z) + "\n";
                            s += "24," + to_string(myJointArr[24].Position.X) + "," + to_string(myJointArr[24].Position.Y) + "," + to_string(myJointArr[24].Position.Z) + "\n";
                            send(clientSocket, (char*)s.c_str(), (int)s.length(), 0);
                            
                        }

                        draw(copy, myJointArr[JointType_Head], myJointArr[JointType_Neck], myMapper);
                        draw(copy, myJointArr[JointType_Neck], myJointArr[JointType_SpineShoulder], myMapper);

                        draw(copy, myJointArr[JointType_SpineShoulder], myJointArr[JointType_ShoulderLeft], myMapper);
                        draw(copy, myJointArr[JointType_SpineShoulder], myJointArr[JointType_SpineMid], myMapper);
                        draw(copy, myJointArr[JointType_SpineShoulder], myJointArr[JointType_ShoulderRight], myMapper);

                        draw(copy, myJointArr[JointType_ShoulderLeft], myJointArr[JointType_ElbowLeft], myMapper);
                        draw(copy, myJointArr[JointType_SpineMid], myJointArr[JointType_SpineBase], myMapper);
                        draw(copy, myJointArr[JointType_ShoulderRight], myJointArr[JointType_ElbowRight], myMapper);

                        draw(copy, myJointArr[JointType_ElbowLeft], myJointArr[JointType_WristLeft], myMapper);
                        draw(copy, myJointArr[JointType_SpineBase], myJointArr[JointType_HipLeft], myMapper);
                        draw(copy, myJointArr[JointType_SpineBase], myJointArr[JointType_HipRight], myMapper);
                        draw(copy, myJointArr[JointType_ElbowRight], myJointArr[JointType_WristRight], myMapper);

                        draw(copy, myJointArr[JointType_WristLeft], myJointArr[JointType_ThumbLeft], myMapper);
                        draw(copy, myJointArr[JointType_WristLeft], myJointArr[JointType_HandLeft], myMapper);
                        draw(copy, myJointArr[JointType_HipLeft], myJointArr[JointType_KneeLeft], myMapper);
                        draw(copy, myJointArr[JointType_HipRight], myJointArr[JointType_KneeRight], myMapper);
                        draw(copy, myJointArr[JointType_WristRight], myJointArr[JointType_ThumbRight], myMapper);
                        draw(copy, myJointArr[JointType_WristRight], myJointArr[JointType_HandRight], myMapper);

                        draw(copy, myJointArr[JointType_HandLeft], myJointArr[JointType_HandTipLeft], myMapper);
                        draw(copy, myJointArr[JointType_KneeLeft], myJointArr[JointType_FootLeft], myMapper);
                        draw(copy, myJointArr[JointType_KneeRight], myJointArr[JointType_FootRight], myMapper);
                        draw(copy, myJointArr[JointType_HandRight], myJointArr[JointType_HandTipRight], myMapper);
                    }
                }
            }
        delete[]myBodyArr;

        myBodyFrame->Release();
        myColorFrame->Release();

        cv::imshow("TEST", copy);

        if (char(waitKey(30)) == 'q') //按q退出,必须删掉opencv_world3416.lib才能生效
        {
            break;
        }

        if (startFlag) {
            std::printf("frame: %d\n", frame);

        }

    }

    //ofs.close();
    myMapper->Release();

    myDescription->Release();
    myColorReader->Release();
    myColorSource->Release();

    myBodyReader->Release();
    myBodySource->Release();
    mySensor->Close();
    mySensor->Release();

    //outputVideo.release();

    return  0;
}


void    draw(Mat& img, Joint& r_1, Joint& r_2, ICoordinateMapper* myMapper)
{
    //用两个关节点来做线段的两端，并且进行状态过滤
    if (r_1.TrackingState == TrackingState_Tracked && r_2.TrackingState == TrackingState_Tracked)
    {
        ColorSpacePoint t_point;    //要把关节点用的摄像机坐标下的点转换成彩色空间的点
        Point   p_1, p_2;
        myMapper->MapCameraPointToColorSpace(r_1.Position, &t_point);
        p_1.x = t_point.X;
        p_1.y = t_point.Y;
        myMapper->MapCameraPointToColorSpace(r_2.Position, &t_point);
        p_2.x = t_point.X;
        p_2.y = t_point.Y;

        line(img, p_1, p_2, Vec3b(0, 255, 0), 5);
        circle(img, p_1, 10, Vec3b(255, 0, 0), -1);
        circle(img, p_2, 10, Vec3b(255, 0, 0), -1);
    }
}

//部分参考：https ://blog.csdn.net/baolinq/article/details/52373574