//  运行环境：
//      Windows11/10
//      Microsoft Visual Studio Community 2019 版本 16.10.2
//      opencv3.416
//      Kinect2.0_1409
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


    VideoWriter outputVideo("output0.mp4", CV_FOURCC('D', 'I', 'V', 'X'), 6.0, frameSize, 1);
    //创建视频文件
    if (!outputVideo.isOpened()) {
        cout << "fail to open the videowriter" << endl;
        system("pause");
        return -1;
    }

    ofstream ofs;
    //创建骨架节点坐标文件
    ofs.open("test0.txt", ios::out);


    //*************************************以上为存储数据集做准备**************************************


    int frame = 0;
    int fileCount = 0;
    int pictureCount = 0;
    bool pictureFlag = 0;
    bool startFlag = 1;//初始状态为录制中

    while (1)
    {
        if (_kbhit())
        {
            int m = _getch();

            if (m == 32 && startFlag == 0) // 按空格开始
            {
                fileCount += 1;
                string filename1 = "output" + to_string(fileCount) + ".mp4";
                //定义writer对象
                outputVideo.open(filename1, CV_FOURCC('D', 'I', 'V', 'X'), 6.0, frameSize, 1);
                //判断open writer对象是否出错
                if (!outputVideo.isOpened()) {
                    cout << "fail to open the videowriter" << endl;
                    system("pause");
                    return -1;
                }
                string filename2 = "test" + to_string(fileCount) + ".txt";
                ofs.open(filename2, ios::out);
                startFlag = 1;
            }

            if (m == 27 && startFlag == 1) // 按Esc结束
            {
                outputVideo.~VideoWriter();
                VideoWriter outputVideo;
                ofs.close();
                startFlag = 0;
            }

            if (m == 49) //按1拍照
            {
                pictureFlag = 1;
            }

        }
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
                        if (startFlag)//如果录制中，就写入骨架坐标
                        {
                            ofs << myJointArr[0].Position.X << myJointArr[0].Position.Y << myJointArr[0].Position.Z <<myJointArr[0].TrackingState << endl;
                            ofs << myJointArr[1].Position.X << myJointArr[1].Position.Y << myJointArr[1].Position.Z <<myJointArr[1].TrackingState << endl;
                            ofs << myJointArr[2].Position.X << myJointArr[2].Position.Y << myJointArr[2].Position.Z <<myJointArr[2].TrackingState << endl;
                            ofs << myJointArr[3].Position.X << myJointArr[3].Position.Y << myJointArr[3].Position.Z <<myJointArr[3].TrackingState << endl;
                            ofs << myJointArr[4].Position.X << myJointArr[4].Position.Y << myJointArr[4].Position.Z <<myJointArr[4].TrackingState << endl;
                            ofs << myJointArr[5].Position.X << myJointArr[5].Position.Y << myJointArr[5].Position.Z <<myJointArr[5].TrackingState << endl;
                            ofs << myJointArr[6].Position.X << myJointArr[6].Position.Y << myJointArr[6].Position.Z <<myJointArr[6].TrackingState << endl;
                            ofs << myJointArr[7].Position.X << myJointArr[7].Position.Y << myJointArr[7].Position.Z <<myJointArr[7].TrackingState << endl;
                            ofs << myJointArr[8].Position.X << myJointArr[8].Position.Y << myJointArr[8].Position.Z <<myJointArr[8].TrackingState << endl;
                            ofs << myJointArr[9].Position.X << myJointArr[9].Position.Y << myJointArr[9].Position.Z <<myJointArr[9].TrackingState << endl;
                            ofs << myJointArr[10].Position.X << myJointArr[10].Position.Y << myJointArr[10].Position.Z <<myJointArr[10].TrackingState << endl;
                            ofs << myJointArr[11].Position.X << myJointArr[11].Position.Y << myJointArr[11].Position.Z <<myJointArr[11].TrackingState << endl;
                            ofs << myJointArr[12].Position.X << myJointArr[12].Position.Y << myJointArr[12].Position.Z <<myJointArr[12].TrackingState << endl;
                            ofs << myJointArr[13].Position.X << myJointArr[13].Position.Y << myJointArr[13].Position.Z <<myJointArr[13].TrackingState << endl;
                            ofs << myJointArr[14].Position.X << myJointArr[14].Position.Y << myJointArr[14].Position.Z <<myJointArr[14].TrackingState << endl;
                            ofs << myJointArr[15].Position.X << myJointArr[15].Position.Y << myJointArr[15].Position.Z <<myJointArr[15].TrackingState << endl;
                            ofs << myJointArr[16].Position.X << myJointArr[16].Position.Y << myJointArr[16].Position.Z <<myJointArr[16].TrackingState << endl;
                            ofs << myJointArr[17].Position.X << myJointArr[17].Position.Y << myJointArr[17].Position.Z <<myJointArr[17].TrackingState << endl;
                            ofs << myJointArr[18].Position.X << myJointArr[18].Position.Y << myJointArr[18].Position.Z <<myJointArr[18].TrackingState << endl;
                            ofs << myJointArr[19].Position.X << myJointArr[19].Position.Y << myJointArr[19].Position.Z <<myJointArr[19].TrackingState << endl;
                            ofs << myJointArr[20].Position.X << myJointArr[20].Position.Y << myJointArr[20].Position.Z <<myJointArr[20].TrackingState << endl;
                            ofs << myJointArr[21].Position.X << myJointArr[21].Position.Y << myJointArr[21].Position.Z <<myJointArr[21].TrackingState << endl;
                            ofs << myJointArr[22].Position.X << myJointArr[22].Position.Y << myJointArr[22].Position.Z <<myJointArr[22].TrackingState << endl;
                            ofs << myJointArr[23].Position.X << myJointArr[23].Position.Y << myJointArr[23].Position.Z <<myJointArr[23].TrackingState << endl;
                            ofs << myJointArr[24].Position.X << myJointArr[24].Position.Y << myJointArr[24].Position.Z <<myJointArr[24].TrackingState << endl;

                        }
                        if (pictureFlag) {
                            ofstream ofs1;//创建骨架节点坐标文件
                            ofs1.open("pictureNode"+ to_string(pictureCount) + ".txt", ios::out);
                            ofs1 << myJointArr[0].Position.X << myJointArr[0].Position.Y << myJointArr[0].Position.Z <<myJointArr[0].TrackingState << endl;
                            ofs1 << myJointArr[1].Position.X << myJointArr[1].Position.Y << myJointArr[1].Position.Z <<myJointArr[1].TrackingState << endl;
                            ofs1 << myJointArr[2].Position.X << myJointArr[2].Position.Y << myJointArr[2].Position.Z <<myJointArr[2].TrackingState << endl;
                            ofs1 << myJointArr[3].Position.X << myJointArr[3].Position.Y << myJointArr[3].Position.Z <<myJointArr[3].TrackingState << endl;
                            ofs1 << myJointArr[4].Position.X << myJointArr[4].Position.Y << myJointArr[4].Position.Z <<myJointArr[4].TrackingState << endl;
                            ofs1 << myJointArr[5].Position.X << myJointArr[5].Position.Y << myJointArr[5].Position.Z <<myJointArr[5].TrackingState << endl;
                            ofs1 << myJointArr[6].Position.X << myJointArr[6].Position.Y << myJointArr[6].Position.Z <<myJointArr[6].TrackingState << endl;
                            ofs1 << myJointArr[7].Position.X << myJointArr[7].Position.Y << myJointArr[7].Position.Z <<myJointArr[7].TrackingState << endl;
                            ofs1 << myJointArr[8].Position.X << myJointArr[8].Position.Y << myJointArr[8].Position.Z <<myJointArr[8].TrackingState << endl;
                            ofs1 << myJointArr[9].Position.X << myJointArr[9].Position.Y << myJointArr[9].Position.Z <<myJointArr[9].TrackingState << endl;
                            ofs1 << myJointArr[10].Position.X << myJointArr[10].Position.Y << myJointArr[10].Position.Z <<myJointArr[10].TrackingState << endl;
                            ofs1 << myJointArr[11].Position.X << myJointArr[11].Position.Y << myJointArr[11].Position.Z <<myJointArr[11].TrackingState << endl;
                            ofs1 << myJointArr[12].Position.X << myJointArr[12].Position.Y << myJointArr[12].Position.Z <<myJointArr[12].TrackingState << endl;
                            ofs1 << myJointArr[13].Position.X << myJointArr[13].Position.Y << myJointArr[13].Position.Z <<myJointArr[13].TrackingState << endl;
                            ofs1 << myJointArr[14].Position.X << myJointArr[14].Position.Y << myJointArr[14].Position.Z <<myJointArr[14].TrackingState << endl;
                            ofs1 << myJointArr[15].Position.X << myJointArr[15].Position.Y << myJointArr[15].Position.Z <<myJointArr[15].TrackingState << endl;
                            ofs1 << myJointArr[16].Position.X << myJointArr[16].Position.Y << myJointArr[16].Position.Z <<myJointArr[16].TrackingState << endl;
                            ofs1 << myJointArr[17].Position.X << myJointArr[17].Position.Y << myJointArr[17].Position.Z <<myJointArr[17].TrackingState << endl;
                            ofs1 << myJointArr[18].Position.X << myJointArr[18].Position.Y << myJointArr[18].Position.Z <<myJointArr[18].TrackingState << endl;
                            ofs1 << myJointArr[19].Position.X << myJointArr[19].Position.Y << myJointArr[19].Position.Z <<myJointArr[19].TrackingState << endl;
                            ofs1 << myJointArr[20].Position.X << myJointArr[20].Position.Y << myJointArr[20].Position.Z <<myJointArr[20].TrackingState << endl;
                            ofs1 << myJointArr[21].Position.X << myJointArr[21].Position.Y << myJointArr[21].Position.Z <<myJointArr[21].TrackingState << endl;
                            ofs1 << myJointArr[22].Position.X << myJointArr[22].Position.Y << myJointArr[22].Position.Z <<myJointArr[22].TrackingState << endl;
                            ofs1 << myJointArr[23].Position.X << myJointArr[23].Position.Y << myJointArr[23].Position.Z <<myJointArr[23].TrackingState << endl;
                            ofs1 << myJointArr[24].Position.X << myJointArr[24].Position.Y << myJointArr[24].Position.Z <<myJointArr[24].TrackingState << endl;
                            ofs1.close();
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

        if (pictureFlag) {
            cv::imwrite("picure" + to_string(pictureCount) + ".jpg", copy);
            pictureCount += 1;
            pictureFlag = 0;
        }

        cv::Mat curVideo;
        cv::cvtColor(copy, curVideo, cv::COLOR_BGRA2BGR);//BGRA去掉A, 不然存不了
        outputVideo << curVideo; //存入这一帧视频
    }

    ofs.close();
    myMapper->Release();

    myDescription->Release();
    myColorReader->Release();
    myColorSource->Release();

    myBodyReader->Release();
    myBodySource->Release();
    mySensor->Close();
    mySensor->Release();

    outputVideo.release();

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