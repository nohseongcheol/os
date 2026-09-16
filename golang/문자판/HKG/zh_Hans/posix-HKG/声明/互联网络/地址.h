/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _声明_互联网络_地址
#define _声明_互联网络_地址

#include <整数类型.h>
#include <系统/通信端点.h>

typedef 无符号32位整数 互联网络地址值类型;
typedef 无符号16位整数 通信端口编号类型;

struct 互联网络地址 {
    互联网络地址值类型 地址值;
};

struct 互联网络端点地址 {
    地址族类型 互联地址族;
    通信端口编号类型 通信端口编号;
    struct 互联网络地址 互联地址内容;
    unsigned char 地址填充区[8];
};

#define 互联网络基本协议 0
#define 用户数据报协议 17
#define 任意本地地址 ((互联网络地址值类型)0x00000000U)
#define 本机回环地址 ((互联网络地址值类型)0x7f000001U)

#endif
