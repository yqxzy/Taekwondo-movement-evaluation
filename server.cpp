#define _WINSOCK_DEPRECATED_NO_WARNINGS 	//比较新版的vs,会警告我们不要使用一
#include <stdio.h>
#include <stdlib.h>
#include<iostream>
#include<string>
#include<cstring>
#include<WS2tcpip.h>
#include <WinSock2.h>						//一般情况下,这个头文件位于windows.h之前,避免发生某些错误
#include<Windows.h>
#include<fstream>
#pragma comment(lib, "ws2_32.lib") 			//显示加载 ws2_32.dll	ws2_32.dll就是最新socket版本啦
using namespace std;
#include<conio.h>


	int main()
	{
	
	//	1	初始化
	WSADATA wsadata;
	WSAStartup(MAKEWORD(2, 2), &wsadata);	//make word,你把鼠标移到WSAStartup看看参数列表,是不是就是一个word啊


	//	2	创建服务器的套接字
	SOCKET serviceSocket;
	serviceSocket = socket(AF_INET, SOCK_STREAM, 0);	//socket(协议族,socket数据传输方式,某个协议)	我们默认为0,其实就是一个宏
	if (SOCKET_ERROR == serviceSocket) {
		cout << "creat fail" << endl;
	}
	else {
		cout << "creat success" << endl;
	}
	//	3	绑定套接字	指定绑定的IP地址和端口号
	sockaddr_in socketAddr;								//一个绑定地址:有IP地址,有端口号,有协议族
	socketAddr.sin_family = AF_INET;
	socketAddr.sin_addr.S_un.S_addr = inet_addr("10.24.81.213");		//代码开头第一行我们定义的宏在这就其作用啦
	socketAddr.sin_port = htons(1234);
	int bRes = bind(serviceSocket, (SOCKADDR*)&socketAddr, sizeof(SOCKADDR));	//绑定注意的一点就是记得强制类型转换
	if (SOCKET_ERROR == bRes) {
		cout << "bind fail" << endl;
	}
	else {
		cout << "bind success" << endl;
	}

	//	4	服务器监听	
	int lLen = listen(serviceSocket, 5);	//监听的第二个参数就是:能存放多少个客户端请求,到并发编程的时候很有用哦
	if (SOCKET_ERROR == lLen) {
		cout << "listen fail" << endl;
	}
	else {
		cout << "listen success" << endl;
	}

	//	5	接受请求
	sockaddr_in revClientAddr;
	SOCKET recvClientSocket = INVALID_SOCKET;	//初始化一个接受的客户端socket
	int _revSize = sizeof(sockaddr_in);
	recvClientSocket = accept(serviceSocket, (SOCKADDR*)&revClientAddr, &_revSize);

	sockaddr_in revClientAddr1;
	SOCKET recvClientSocket1 = INVALID_SOCKET;	//初始化一个接受的客户端socket
	int _revSize1 = sizeof(sockaddr_in);
	recvClientSocket1 = accept(serviceSocket, (SOCKADDR*)&revClientAddr1, &_revSize1);


	if (INVALID_SOCKET == recvClientSocket) {
		cout << "sever request error" << endl;
	}
	else {
		cout << "sever request success" << endl;
	}
	
	if (INVALID_SOCKET == recvClientSocket1) {
		cout << "sever request error" << endl;
	}
	else {
		cout << "sever request success" << endl;
	}

	ofstream ofs;
	ofstream ofs1;
	//创建骨架节点坐标文件


	int fileCount = 0;
	int startFlag = 0;
	int pictureCount = 0;

	//	6	发送/接受 数据
	while (true) {

		char recvBuf[4024] = {};
		int reLen = recv(recvClientSocket, recvBuf, 4024, 0);
		char recvBuf1[4024] = {};
		int reLen1 = recv(recvClientSocket1, recvBuf1, 4024, 0);
		//int sLen = send(recvClientSocket, recvBuf, reLen, 0);
		if (SOCKET_ERROR == reLen) {
			cout << "send error" << endl;
		}
		else {
			//cout << recvBuf << endl << endl;
			reLen = SOCKET_ERROR;
		}
		if (SOCKET_ERROR == reLen1) {
			cout << "send error" << endl;
		}
		else {
			//cout << recvBuf << endl << endl;
			reLen1 = SOCKET_ERROR;
		}
		if (startFlag == 1)
		{
			ofs << recvBuf << endl;
			cout << recvBuf << endl << endl;
			ofs1 << recvBuf1 << endl;
			cout << recvBuf1 << endl << endl;
		}
		if (_kbhit())
		{
			int m = _getch();
			if (m == 32 && startFlag == 0) // 按空格开始
			{

				cout << "================================start================================" << endl;
				fileCount += 1;
				string filename = "test" + to_string(fileCount) + ".txt";
				ofs.open(filename, ios::out);
				string filename1 = "test" + to_string(fileCount) + "_1" + ".txt";
				ofs1.open(filename1, ios::out);
				startFlag = 1;
			}

			if (m == 27 && startFlag == 1) // 按Esc结束
			{
				cout << "================================end==================================" << endl;
				ofs.close();
				ofs1.close();
				startFlag = 0;
			}
			if (m == 49) //按1拍照
			{
				pictureCount++;
				string filename = "picture" + to_string(pictureCount) + ".txt";
				ofs.open(filename, ios::out);
				string filename1 = "picture" + to_string(pictureCount) + "_1" + ".txt";
				ofs1.open(filename1, ios::out);
				ofs << recvBuf << endl;
				ofs1 << recvBuf1 << endl;
				cout << "==================================picture=================================" << endl;
			}
		}
	}

		//	7	关闭socket
		closesocket(recvClientSocket);
		closesocket(recvClientSocket1);


		closesocket(serviceSocket);


		//	8	终止
		WSACleanup();

		cout << "sever stop" << endl;
		cin.get();
		return 0;
	}