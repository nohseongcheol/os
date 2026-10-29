// 동일 中文 헤더를 사용하는 별도 EL0 库. 内核值 직접 호출판과 혼합 禁用值.
#include "文件ABI.h"
#include "调用.h"
#include "网络ABI.h"
static int 错误代码;
int *pk_errno_location(void) { return &错误代码; }
static intptr_t 已检查(intptr_t 结果) { if (结果 < 0) { 错误代码 = -结果; return -1; } return 结果; }
int pk_open(const char *path, int flags, ...) { return 已检查(用户调用(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
输入输出结果类型 pk_read(int fd, void *p, size_t n) { return 已检查(用户调用(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
输入输出结果类型 pk_write(int fd, const void *p, size_t n) { return 已检查(用户调用(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 已检查(用户调用(4, fd, 0, 0, 0, 0, 0)); }
文件偏移类型 pk_lseek(int fd, 文件偏移类型 offset, int origin) { return 已检查(用户调用(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 已检查(用户调用(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, 文件偏移类型 size) { return 已检查(用户调用(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return 已检查(用户调用(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return 已检查(用户调用(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return 已检查(用户调用(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 已检查(用户调用(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 已检查(用户调用(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 已检查(用户调用(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 已检查(用户调用(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return 已检查(用户调用(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return 已检查(用户调用(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return 已检查(用户调用(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* 中文 공개 함수의 实际数据 EL0 实现. 구조체는 SVC에서 复制值·검증한다. */
int 创建端点(int 地址族,int 通信模式,int 传送协议) {
    return 已检查(用户调用(32,地址族,通信模式,传送协议,0,0,0));
}
int 绑定地址(int 端点,const struct 套接字地址 *地址,套接字地址长度类型 长度) {
    return 已检查(用户调用(33,端点,(uintptr_t)地址,长度,0,0,0));
}
intptr_t 发送数据报数据(int 端点,const void *数据,size_t 项目个数,int 选中状态值,const struct 套接字地址 *地址,套接字地址长度类型 长度) {
    return 已检查(用户调用(34,端点,(uintptr_t)数据,项目个数,选中状态值,(uintptr_t)地址,长度));
}
intptr_t 接收数据报数据(int 端点,void *数据,size_t 项目个数,int 选中状态值,struct 套接字地址 *地址,套接字地址长度类型 *长度) {
    return 已检查(用户调用(35,端点,(uintptr_t)数据,项目个数,选中状态值,(uintptr_t)地址,(uintptr_t)长度));
}
int 读取套接字地址(int 端点,struct 套接字地址 *地址,套接字地址长度类型 *长度) {
    return 已检查(用户调用(36,端点,(uintptr_t)地址,(uintptr_t)长度,0,0,0));
}
int 连接网络(int 端点,const struct 套接字地址 *地址,套接字地址长度类型 长度) {
    return 已检查(用户调用(37,端点,(uintptr_t)地址,长度,0,0,0));
}
int 等待状态用于网络连接状态(int 端点,int 等待中个数) {
    return 已检查(用户调用(38,端点,等待中个数,0,0,0,0));
}
int 接受网络连接状态(int 端点,struct 套接字地址 *地址,套接字地址长度类型 *长度) {
    return 已检查(用户调用(39,端点,(uintptr_t)地址,(uintptr_t)长度,0,0,0));
}

/* 文件 함수도 독립된 中文 函数 심볼로 제공한다. */
int 打开文件(const char *路径,int 方法模式,...) { return 已检查(用户调用(3,(uintptr_t)路径,方法模式,0,0,0,0)); }
输入输出结果类型 读取文件数据(int 文件,void *数据,size_t 项目个数) { return 已检查(用户调用(2,文件,(uintptr_t)数据,项目个数,0,0,0)); }
输入输出结果类型 写入文件数据(int 文件,const void *数据,size_t 项目个数) { return 已检查(用户调用(1,文件,(uintptr_t)数据,项目个数,0,0,0)); }
int 关闭文件(int 文件) { return 已检查(用户调用(4,文件,0,0,0,0,0)); }
文件偏移类型 寻道文件(int 文件,文件偏移类型 距离值,int 项目根) { return 已检查(用户调用(5,文件,距离值,项目根,0,0,0)); }
int 移除文件条目名称(const char *路径) { return 已检查(用户调用(11,(uintptr_t)路径,0,0,0,0,0)); }
int 设定文件长度(int 文件,文件偏移类型 大小) { return 已检查(用户调用(10,文件,大小,0,0,0,0)); }
int 提交文件存储装置(int 文件) { return 已检查(用户调用(12,文件,0,0,0,0,0)); }
int 文件大小(int 文件) { return 已检查(用户调用(9,文件,0,0,0,0,0)); }
