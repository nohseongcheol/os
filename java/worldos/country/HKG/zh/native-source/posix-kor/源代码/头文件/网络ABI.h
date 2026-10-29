#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 创建端点 socket
#define 绑定地址 bind
#define 发送数据报数据 sendto
#define 接收数据报数据 recvfrom
#define 读取套接字地址 getsockname
#define 更改网络设置 setsockopt
#define 解析网络地址 inet_pton
#define 格式网络地址 inet_ntop
#define 网络短整数 htons
#define 网络整数 htonl
#define 设备排序短整数 ntohs
#define 设备排序整数 ntohl
#endif
