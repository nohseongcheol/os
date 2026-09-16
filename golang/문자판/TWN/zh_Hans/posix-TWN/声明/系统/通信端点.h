/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _声明_系统_通信端点
#define _声明_系统_通信端点

#include <基本定义.h>
#include <系统/数据类型.h>

typedef unsigned short 地址族类型;

struct 通信端点地址 {
    地址族类型 端点地址族;
    char 地址数据[14];
};

#define 未指定地址族 0
#define 互联网络地址族 2
#define 互联网络协议族 互联网络地址族

#define 数据流端点 1
#define 数据报端点 2

#define 停止接收 0
#define 停止发送 1
#define 停止双向通信 2

#ifdef __cplusplus
extern "C" {
#endif
int 创建通信端点(int 地址族, int 端点类型, int 通信协议);
int 绑定本地地址(int 文件描述编号, const struct 通信端点地址 *地址, 地址长度类型 地址大小);
int 连接对端(int 文件描述编号, const struct 通信端点地址 *地址, 地址长度类型 地址大小);
int 准备接收连接(int 文件描述编号, int 等待上限);
int 接受连接(int 文件描述编号, struct 通信端点地址 *地址, 地址长度类型 *地址大小);
int 取得本地端点地址(int 文件描述编号, struct 通信端点地址 *地址, 地址长度类型 *地址大小);
int 取得对端地址(int 文件描述编号, struct 通信端点地址 *地址, 地址长度类型 *地址大小);
有符号大小类型 发送(int 文件描述编号, const void *数据缓冲区域, 大小类型 长度, int 处理标志);
有符号大小类型 接收(int 文件描述编号, void *数据缓冲区域, 大小类型 长度, int 处理标志);
有符号大小类型 向目的地址发送(int 文件描述编号, const void *报文, 大小类型 长度, int 处理标志,
               const struct 通信端点地址 *目的地址, 地址长度类型 目的地址长度);
有符号大小类型 接收并取得来源地址(int 文件描述编号, void *数据缓冲区域, 大小类型 长度, int 处理标志,
                 struct 通信端点地址 *地址, 地址长度类型 *地址大小);
int 关闭通信方向(int 文件描述编号, int 关闭方向);
int 设置通信端点选项(int 文件描述编号, int 设置层级, int 选项名,
               const void *选项值, 地址长度类型 选项长度);
#ifdef __cplusplus
}
#endif

#endif
