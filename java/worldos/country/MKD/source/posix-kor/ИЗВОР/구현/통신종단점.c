#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *адреса, socklen_t адреса_должина) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)адреса, адреса_должина, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *податоци, size_t бајт_COUNT, int Подесувања,
               const struct sockaddr *адреса, socklen_t адреса_должина) {
    int Барање_на_HTTP[2] = {(int)адреса, адреса_должина};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)податоци, бајт_COUNT, Подесувања, (int)Барање_на_HTTP));
}
ssize_t recvfrom(int 파일서술자, void *податоци, size_t бајт_COUNT, int Подесувања,
                 struct sockaddr *адреса, socklen_t *адреса_должина) {
    int Барање_на_HTTP[2] = {(int)адреса, (int)адреса_должина};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)податоци, бајт_COUNT, Подесувања, (int)Барање_на_HTTP));
}
int getsockname(int 파일서술자, struct sockaddr *адреса, socklen_t *адреса_должина) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)адреса, (int)адреса_должина, 0, 0));
}
int setsockopt(int 파일서술자, int слој_VALUE_e65604ef, int Параметри_име, const void *VALUE, socklen_t VALUE_должина) {
    if (слој_VALUE_e65604ef != SOL_SOCKET || Параметри_име != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_должина != sizeof(struct timeval)) { errno = EINVAL; return -1; }
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
int inet_pton(int 주소체계, const char *низа_VALUE_6ca8363c, void *адреса) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!низа_VALUE_6ca8363c || !адреса) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int отвор_внес = 0; отвор_внес < 4; отвор_внес++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Изврши_2 = низа_VALUE_6ca8363c;
        while (*низа_VALUE_6ca8363c >= '0' && *низа_VALUE_6ca8363c <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *низа_VALUE_6ca8363c++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Изврши_2 == '0')) return 0;
        임시[отвор_внес] = VALUE;
        if (отвор_внес < 3) { if (*низа_VALUE_6ca8363c++ != '.') return 0; }
        else if (*низа_VALUE_6ca8363c) return 0;
    }
    for (int отвор_внес = 0; отвор_внес < 4; отвор_внес++) ((unsigned char *)адреса)[отвор_внес] = 임시[отвор_внес];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *адреса, char *низа_VALUE_6ca8363c, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!адреса || !низа_VALUE_6ca8363c) { errno = EFAULT; return 0; }
    const unsigned char *수 = адреса;
    char 임시[16]; unsigned int должина_VALUE = 0;
    for (int отвор_внес = 0; отвор_внес < 4; отвор_внес++) {
        unsigned int VALUE = 수[отвор_внес];
        if (VALUE >= 100) 임시[должина_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[должина_VALUE++] = '0' + VALUE / 10 % 10;
        임시[должина_VALUE++] = '0' + VALUE % 10;
        if (отвор_внес < 3) 임시[должина_VALUE++] = '.';
    }
    임시[должина_VALUE++] = 0;
    if (용량 < должина_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int отвор_внес = 0; отвор_внес < должина_VALUE; отвор_внес++) низа_VALUE_6ca8363c[отвор_внес] = 임시[отвор_внес];
    return низа_VALUE_6ca8363c;
}
