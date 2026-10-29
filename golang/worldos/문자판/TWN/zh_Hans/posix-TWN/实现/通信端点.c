#include <通信地址/字节顺序.h>
#include <系统/系统调用.h>
#include <系统/通信端点.h>

enum { 通信端点系统调用编号 = 102 };
enum {
    通信端点_创建通信端点 = 1, 通信端点_绑定本地地址 = 2, 通信端点_连接对端 = 3, 通信端点_准备接收连接 = 4,
    通信端点_接受连接 = 5, 通信端点_取得本地端点地址 = 6, 通信端点_取得对端地址 = 7,
    通信端点_发送 = 9, 通信端点_接收 = 10, 通信端点_向目的地址发送 = 11, 通信端点_接收并取得来源地址 = 12,
    通信端点_关闭通信方向 = 13, 通信端点_设置通信端点选项 = 14
};

static long 调用通信端点(long 通信调用编号, unsigned long *传入参数列表)
{
    return __syscall_result(
        __syscall6(通信端点系统调用编号, 通信调用编号, (long)传入参数列表, 0, 0, 0, 0));
}

无符号16位整数 转为网络次序16位(无符号16位整数 值) { return (无符号16位整数)((值 << 8) | (值 >> 8)); }
无符号16位整数 转为主机次序16位(无符号16位整数 值) { return 转为网络次序16位(值); }
无符号32位整数 转为网络次序32位(无符号32位整数 值)
{
    return ((值 & 0x000000ffU) << 24) | ((值 & 0x0000ff00U) << 8) |
           ((值 & 0x00ff0000U) >> 8) | ((值 & 0xff000000U) >> 24);
}
无符号32位整数 转为主机次序32位(无符号32位整数 值) { return 转为网络次序32位(值); }

int 创建通信端点(int 地址族, int 端点类型, int 通信协议)
{
    unsigned long 传值数组[3] = {(unsigned long)地址族, (unsigned long)端点类型, (unsigned long)通信协议};
    return (int)调用通信端点(通信端点_创建通信端点, 传值数组);
}

int 绑定本地地址(int 文件描述编号, const struct 通信端点地址 *地址, 地址长度类型 长度)
{
    unsigned long 传值数组[3] = {(unsigned long)文件描述编号, (unsigned long)地址, 长度};
    return (int)调用通信端点(通信端点_绑定本地地址, 传值数组);
}

int 连接对端(int 文件描述编号, const struct 通信端点地址 *地址, 地址长度类型 长度)
{
    unsigned long 传值数组[3] = {(unsigned long)文件描述编号, (unsigned long)地址, 长度};
    return (int)调用通信端点(通信端点_连接对端, 传值数组);
}

int 准备接收连接(int 文件描述编号, int 等待上限)
{
    unsigned long 传值数组[2] = {(unsigned long)文件描述编号, (unsigned long)等待上限};
    return (int)调用通信端点(通信端点_准备接收连接, 传值数组);
}

int 接受连接(int 文件描述编号, struct 通信端点地址 *地址, 地址长度类型 *长度)
{
    unsigned long 传值数组[3] = {(unsigned long)文件描述编号, (unsigned long)地址, (unsigned long)长度};
    return (int)调用通信端点(通信端点_接受连接, 传值数组);
}

int 取得本地端点地址(int 文件描述编号, struct 通信端点地址 *地址, 地址长度类型 *长度)
{
    unsigned long 传值数组[3] = {(unsigned long)文件描述编号, (unsigned long)地址, (unsigned long)长度};
    return (int)调用通信端点(通信端点_取得本地端点地址, 传值数组);
}

int 取得对端地址(int 文件描述编号, struct 通信端点地址 *地址, 地址长度类型 *长度)
{
    unsigned long 传值数组[3] = {(unsigned long)文件描述编号, (unsigned long)地址, (unsigned long)长度};
    return (int)调用通信端点(通信端点_取得对端地址, 传值数组);
}

有符号大小类型 发送(int 文件描述编号, const void *数据缓冲区域, 大小类型 长度, int 处理标志)
{
    unsigned long 传值数组[4] = {(unsigned long)文件描述编号, (unsigned long)数据缓冲区域, 长度, (unsigned long)处理标志};
    return (有符号大小类型)调用通信端点(通信端点_发送, 传值数组);
}

有符号大小类型 接收(int 文件描述编号, void *数据缓冲区域, 大小类型 长度, int 处理标志)
{
    unsigned long 传值数组[4] = {(unsigned long)文件描述编号, (unsigned long)数据缓冲区域, 长度, (unsigned long)处理标志};
    return (有符号大小类型)调用通信端点(通信端点_接收, 传值数组);
}

有符号大小类型 向目的地址发送(int 文件描述编号, const void *数据缓冲区域, 大小类型 长度, int 处理标志,
               const struct 通信端点地址 *地址, 地址长度类型 地址长度)
{
    unsigned long 传值数组[6] = {(unsigned long)文件描述编号, (unsigned long)数据缓冲区域, 长度,
                          (unsigned long)处理标志, (unsigned long)地址, 地址长度};
    return (有符号大小类型)调用通信端点(通信端点_向目的地址发送, 传值数组);
}

有符号大小类型 接收并取得来源地址(int 文件描述编号, void *数据缓冲区域, 大小类型 长度, int 处理标志,
                 struct 通信端点地址 *地址, 地址长度类型 *地址长度)
{
    unsigned long 传值数组[6] = {(unsigned long)文件描述编号, (unsigned long)数据缓冲区域, 长度,
                          (unsigned long)处理标志, (unsigned long)地址,
                          (unsigned long)地址长度};
    return (有符号大小类型)调用通信端点(通信端点_接收并取得来源地址, 传值数组);
}

int 关闭通信方向(int 文件描述编号, int 关闭方向)
{
    unsigned long 传值数组[2] = {(unsigned long)文件描述编号, (unsigned long)关闭方向};
    return (int)调用通信端点(通信端点_关闭通信方向, 传值数组);
}

int 设置通信端点选项(int 文件描述编号, int 设置层级, int 选项名,
               const void *选项值, 地址长度类型 选项长度)
{
    unsigned long 传值数组[5] = {(unsigned long)文件描述编号, (unsigned long)设置层级,
                          (unsigned long)选项名, (unsigned long)选项值,
                          选项长度};
    return (int)调用通信端点(通信端点_设置通信端点选项, 传值数组);
}
