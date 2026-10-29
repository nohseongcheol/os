#include <網路ABI.h>
#include <errno.h>
#include "呼叫邊界位置.h"

int socket(int 地址方案, int 網路種類, int 契約編號) {
    return 調用狀態結果(jkoros_syscall(41, 地址方案, 網路種類, 契約編號, 0, 0));
}
int bind(int 檔案描述符, const struct sockaddr *地址, socklen_t 地址長度) {
    return 調用狀態結果(jkoros_syscall(42, 檔案描述符, (int)地址, 地址長度, 0, 0));
}
ssize_t sendto(int 檔案描述符, const void *資料, size_t 位元組個數, int 設置,
               const struct sockaddr *地址, socklen_t 地址長度) {
    int 申請[2] = {(int)地址, 地址長度};
    return 調用狀態結果(jkoros_syscall(43, 檔案描述符, (int)資料, 位元組個數, 設置, (int)申請));
}
ssize_t recvfrom(int 檔案描述符, void *資料, size_t 位元組個數, int 設置,
                 struct sockaddr *地址, socklen_t *地址長度) {
    int 申請[2] = {(int)地址, (int)地址長度};
    return 調用狀態結果(jkoros_syscall(44, 檔案描述符, (int)資料, 位元組個數, 設置, (int)申請));
}
int getsockname(int 檔案描述符, struct sockaddr *地址, socklen_t *地址長度) {
    return 調用狀態結果(jkoros_syscall(45, 檔案描述符, (int)地址, (int)地址長度, 0, 0));
}
int setsockopt(int 檔案描述符, int 層值, int 設置名稱, const void *值, socklen_t 值長度) {
    if (層值 != SOL_SOCKET || 設置名稱 != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!值) { errno = EFAULT; return -1; }
    if (值長度 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *時間值 = 值;
    if (時間值->tv_sec < 0 || 時間值->tv_sec > 2 || 時間值->tv_usec < 0 || 時間值->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 毫秒 = 時間值->tv_sec * 1000 + (時間值->tv_usec + 999) / 1000;
    return 調用狀態結果(jkoros_syscall(46, 檔案描述符, 毫秒, 0, 0, 0));
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
    unsigned char 臨時值[4];
    for (int 槽條目 = 0; 槽條目 < 4; 槽條目++) {
        int 值 = 0, 位數 = 0;
        const char *運行 = 字符串;
        while (*字符串 >= '0' && *字符串 <= '9') {
            if (++位數 > 3) return 0;
            值 = 值 * 10 + *字符串++ - '0';
        }
        if (!位數 || 值 > 255 || (位數 > 1 && *運行 == '0')) return 0;
        臨時值[槽條目] = 值;
        if (槽條目 < 3) { if (*字符串++ != '.') return 0; }
        else if (*字符串) return 0;
    }
    for (int 槽條目 = 0; 槽條目 < 4; 槽條目++) ((unsigned char *)地址)[槽條目] = 臨時值[槽條目];
    return 1;
}
const char *inet_ntop(int 地址方案, const void *地址, char *字符串, socklen_t 容量值) {
    if (地址方案 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!地址 || !字符串) { errno = EFAULT; return 0; }
    const unsigned char *數 = 地址;
    char 臨時值[16]; unsigned int 長度 = 0;
    for (int 槽條目 = 0; 槽條目 < 4; 槽條目++) {
        unsigned int 值 = 數[槽條目];
        if (值 >= 100) 臨時值[長度++] = '0' + 值 / 100;
        if (值 >= 10) 臨時值[長度++] = '0' + 值 / 10 % 10;
        臨時值[長度++] = '0' + 值 % 10;
        if (槽條目 < 3) 臨時值[長度++] = '.';
    }
    臨時值[長度++] = 0;
    if (容量值 < 長度) { errno = ENOSPC; return 0; }
    for (unsigned int 槽條目 = 0; 槽條目 < 長度; 槽條目++) 字符串[槽條目] = 臨時值[槽條目];
    return 字符串;
}
