#include <网络ABI.h>
#include <errno.h>
#include "调用边界位置.h"

int socket(int 地址方案, int 网络种类, int 契约编号) {
    return 调用状态结果(jkoros_syscall(41, 地址方案, 网络种类, 契约编号, 0, 0));
}
int bind(int 文件描述符, const struct sockaddr *地址, socklen_t 地址长度) {
    return 调用状态结果(jkoros_syscall(42, 文件描述符, (int)地址, 地址长度, 0, 0));
}
ssize_t sendto(int 文件描述符, const void *数据, size_t 字节个数, int 设置,
               const struct sockaddr *地址, socklen_t 地址长度) {
    int 申请[2] = {(int)地址, 地址长度};
    return 调用状态结果(jkoros_syscall(43, 文件描述符, (int)数据, 字节个数, 设置, (int)申请));
}
ssize_t recvfrom(int 文件描述符, void *数据, size_t 字节个数, int 设置,
                 struct sockaddr *地址, socklen_t *地址长度) {
    int 申请[2] = {(int)地址, (int)地址长度};
    return 调用状态结果(jkoros_syscall(44, 文件描述符, (int)数据, 字节个数, 设置, (int)申请));
}
int getsockname(int 文件描述符, struct sockaddr *地址, socklen_t *地址长度) {
    return 调用状态结果(jkoros_syscall(45, 文件描述符, (int)地址, (int)地址长度, 0, 0));
}
int setsockopt(int 文件描述符, int 层值, int 设置名称, const void *值, socklen_t 值长度) {
    if (层值 != SOL_SOCKET || 设置名称 != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!值) { errno = EFAULT; return -1; }
    if (值长度 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *时间值 = 值;
    if (时间值->tv_sec < 0 || 时间值->tv_sec > 2 || 时间值->tv_usec < 0 || 时间值->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 毫秒 = 时间值->tv_sec * 1000 + (时间值->tv_usec + 999) / 1000;
    return 调用状态结果(jkoros_syscall(46, 文件描述符, 毫秒, 0, 0, 0));
}
uint16_t htons(uint16_t 值) { return (值 << 8) | (值 >> 8); }
uint16_t ntohs(uint16_t 值) { return htons(值); }
uint32_t htonl(uint32_t 值) {
    return (值 << 24) | ((值 << 8) & 0xff0000U) | ((值 >> 8) & 0xff00U) | (值 >> 24);
}
uint32_t ntohl(uint32_t 值) { return htonl(值); }
int inet_pton(int 地址方案, const char *字符串, void *地址) {
    if (地址方案 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!字符串 || !地址) { errno = EFAULT; return -1; }
    unsigned char 临时值[4];
    for (int 槽条目 = 0; 槽条目 < 4; 槽条目++) {
        int 值 = 0, 位数 = 0;
        const char *运行 = 字符串;
        while (*字符串 >= '0' && *字符串 <= '9') {
            if (++位数 > 3) return 0;
            值 = 值 * 10 + *字符串++ - '0';
        }
        if (!位数 || 值 > 255 || (位数 > 1 && *运行 == '0')) return 0;
        临时值[槽条目] = 值;
        if (槽条目 < 3) { if (*字符串++ != '.') return 0; }
        else if (*字符串) return 0;
    }
    for (int 槽条目 = 0; 槽条目 < 4; 槽条目++) ((unsigned char *)地址)[槽条目] = 临时值[槽条目];
    return 1;
}
const char *inet_ntop(int 地址方案, const void *地址, char *字符串, socklen_t 容量值) {
    if (地址方案 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!地址 || !字符串) { errno = EFAULT; return 0; }
    const unsigned char *数 = 地址;
    char 临时值[16]; unsigned int 长度 = 0;
    for (int 槽条目 = 0; 槽条目 < 4; 槽条目++) {
        unsigned int 值 = 数[槽条目];
        if (值 >= 100) 临时值[长度++] = '0' + 值 / 100;
        if (值 >= 10) 临时值[长度++] = '0' + 值 / 10 % 10;
        临时值[长度++] = '0' + 值 % 10;
        if (槽条目 < 3) 临时值[长度++] = '.';
    }
    临时值[长度++] = 0;
    if (容量值 < 长度) { errno = ENOSPC; return 0; }
    for (unsigned int 槽条目 = 0; 槽条目 < 长度; 槽条目++) 字符串[槽条目] = 临时值[槽条目];
    return 字符串;
}
