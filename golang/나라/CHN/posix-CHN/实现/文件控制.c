/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <文件控制.h>
#include <系统/系统调用.h>

enum { 系统调用_打开 = 5, 系统调用_创建文件 = 8, 系统调用_控制文件 = 55 };

int 打开(const char *路径, int 打开选项, ...)
{
    文件模式类型 访问方式 = 0;
    if ((打开选项 & 不存在则创建) != 0) {
        __builtin_va_list 可变参数;
        __builtin_va_start(可变参数, 打开选项);
        访问方式 = __builtin_va_arg(可变参数, 文件模式类型);
        __builtin_va_end(可变参数);
    }
    return (int)__syscall_result(
        __syscall6(系统调用_打开, (long)路径, 打开选项, 访问方式, 0, 0, 0));
}

int 创建文件(const char *路径, 文件模式类型 访问方式)
{
    return (int)__syscall_result(
        __syscall6(系统调用_创建文件, (long)路径, 访问方式, 0, 0, 0, 0));
}

int 控制文件(int 文件描述编号, int 控制命令, ...)
{
    long 参数值 = 0;
    if (控制命令 == 复制描述编号 || 控制命令 == 设置描述编号标志 || 控制命令 == 设置文件状态标志) {
        __builtin_va_list 可变参数;
        __builtin_va_start(可变参数, 控制命令);
        参数值 = __builtin_va_arg(可变参数, long);
        __builtin_va_end(可变参数);
    }
    return (int)__syscall_result(
        __syscall6(系统调用_控制文件, 文件描述编号, 控制命令, 参数值, 0, 0, 0));
}
