#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *адрес, socklen_t адрес_озынлык) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)адрес, адрес_озынлык, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *мәгълүмат, size_t байт_COUNT, int Caylaw,
               const struct sockaddr *адрес, socklen_t адрес_озынлык) {
    int 요청[2] = {(int)адрес, адрес_озынлык};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)мәгълүмат, байт_COUNT, Caylaw, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *мәгълүмат, size_t байт_COUNT, int Caylaw,
                 struct sockaddr *адрес, socklen_t *адрес_озынлык) {
    int 요청[2] = {(int)адрес, (int)адрес_озынлык};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)мәгълүмат, байт_COUNT, Caylaw, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *адрес, socklen_t *адрес_озынлык) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)адрес, (int)адрес_озынлык, 0, 0));
}
int setsockopt(int 파일서술자, int дәрәҗә_VALUE, int Параметрлар_исем, const void *VALUE, socklen_t VALUE_озынлык) {
    if (дәрәҗә_VALUE != SOL_SOCKET || Параметрлар_исем != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_озынлык != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *TIME_VALUE = VALUE;
    if (TIME_VALUE->tv_sec < 0 || TIME_VALUE->tv_sec > 2 || TIME_VALUE->tv_usec < 0 || TIME_VALUE->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = TIME_VALUE->tv_sec * 1000 + (TIME_VALUE->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VALUE) { return (VALUE << 8) | (VALUE >> 8); }
uint16_t ntohs(uint16_t VALUE) { return htons(VALUE); }
uint32_t htonl(uint32_t VALUE) {
    return (VALUE << 24) | ((VALUE << 8) & 0xff0000U) | ((VALUE >> 8) & 0xff00U) | (VALUE >> 24);
}
uint32_t ntohl(uint32_t VALUE) { return htonl(VALUE); }
int inet_pton(int 주소체계, const char *юл_VALUE_6ca8363c, void *адрес) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!юл_VALUE_6ca8363c || !адрес) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int оя_кертү = 0; оя_кертү < 4; оя_кертү++) {
        int VALUE = 0, 자릿수 = 0;
        const char *эшләтү = юл_VALUE_6ca8363c;
        while (*юл_VALUE_6ca8363c >= '0' && *юл_VALUE_6ca8363c <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *юл_VALUE_6ca8363c++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *эшләтү == '0')) return 0;
        임시[оя_кертү] = VALUE;
        if (оя_кертү < 3) { if (*юл_VALUE_6ca8363c++ != '.') return 0; }
        else if (*юл_VALUE_6ca8363c) return 0;
    }
    for (int оя_кертү = 0; оя_кертү < 4; оя_кертү++) ((unsigned char *)адрес)[оя_кертү] = 임시[оя_кертү];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *адрес, char *юл_VALUE_6ca8363c, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!адрес || !юл_VALUE_6ca8363c) { errno = EFAULT; return 0; }
    const unsigned char *수 = адрес;
    char 임시[16]; unsigned int озынлык_VALUE = 0;
    for (int оя_кертү = 0; оя_кертү < 4; оя_кертү++) {
        unsigned int VALUE = 수[оя_кертү];
        if (VALUE >= 100) 임시[озынлык_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[озынлык_VALUE++] = '0' + VALUE / 10 % 10;
        임시[озынлык_VALUE++] = '0' + VALUE % 10;
        if (оя_кертү < 3) 임시[озынлык_VALUE++] = '.';
    }
    임시[озынлык_VALUE++] = 0;
    if (용량 < озынлык_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int оя_кертү = 0; оя_кертү < озынлык_VALUE; оя_кертү++) юл_VALUE_6ca8363c[оя_кертү] = 임시[оя_кертү];
    return юл_VALUE_6ca8363c;
}
