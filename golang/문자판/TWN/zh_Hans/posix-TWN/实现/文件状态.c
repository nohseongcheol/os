/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <系统/文件状态.h>
#include <系统/系统身份.h>
#include <系统/系统调用.h>

enum { 系统调用_文件状态 = 106, 系统调用_取得链接自身状态 = 107, 系统调用_取得打开文件状态 = 108, 系统调用_取得系统信息 = 122 };

int 文件状态(const char *路径, struct 文件状态 *缓冲区域)
{
    return (int)__syscall_result(
        __syscall6(系统调用_文件状态, (long)路径, (long)缓冲区域, 0, 0, 0, 0));
}

int 取得链接自身状态(const char *路径, struct 文件状态 *缓冲区域)
{
    return (int)__syscall_result(
        __syscall6(系统调用_取得链接自身状态, (long)路径, (long)缓冲区域, 0, 0, 0, 0));
}

int 取得打开文件状态(int 文件描述编号, struct 文件状态 *缓冲区域)
{
    return (int)__syscall_result(
        __syscall6(系统调用_取得打开文件状态, 文件描述编号, (long)缓冲区域, 0, 0, 0, 0));
}

int 取得系统信息(struct 系统身份信息 *系统资料)
{
    return (int)__syscall_result(
        __syscall6(系统调用_取得系统信息, (long)系统资料, 0, 0, 0, 0, 0));
}
