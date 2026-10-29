#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ADDRESS, socklen_t ADDRESS_lengd) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ADDRESS, ADDRESS_lengd, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t byte_COUNT, int Innstillingar,
               const struct sockaddr *ADDRESS, socklen_t ADDRESS_lengd) {
    int 요청[2] = {(int)ADDRESS, ADDRESS_lengd};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, byte_COUNT, Innstillingar, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t byte_COUNT, int Innstillingar,
                 struct sockaddr *ADDRESS, socklen_t *ADDRESS_lengd) {
    int 요청[2] = {(int)ADDRESS, (int)ADDRESS_lengd};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, byte_COUNT, Innstillingar, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ADDRESS, socklen_t *ADDRESS_lengd) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ADDRESS, (int)ADDRESS_lengd, 0, 0));
}
int setsockopt(int 파일서술자, int lag_VALUE, int Innstillingar_namn, const void *VALUE, socklen_t VALUE_lengd) {
    if (lag_VALUE != SOL_SOCKET || Innstillingar_namn != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_lengd != sizeof(struct timeval)) { errno = EINVAL; return -1; }
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
int inet_pton(int 주소체계, const char *streng_VALUE, void *ADDRESS) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!streng_VALUE || !ADDRESS) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int felt_oppføring = 0; felt_oppføring < 4; felt_oppføring++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Køyr_2 = streng_VALUE;
        while (*streng_VALUE >= '0' && *streng_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *streng_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Køyr_2 == '0')) return 0;
        임시[felt_oppføring] = VALUE;
        if (felt_oppføring < 3) { if (*streng_VALUE++ != '.') return 0; }
        else if (*streng_VALUE) return 0;
    }
    for (int felt_oppføring = 0; felt_oppføring < 4; felt_oppføring++) ((unsigned char *)ADDRESS)[felt_oppføring] = 임시[felt_oppføring];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ADDRESS, char *streng_VALUE, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ADDRESS || !streng_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = ADDRESS;
    char 임시[16]; unsigned int lengd_VALUE = 0;
    for (int felt_oppføring = 0; felt_oppføring < 4; felt_oppføring++) {
        unsigned int VALUE = 수[felt_oppføring];
        if (VALUE >= 100) 임시[lengd_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[lengd_VALUE++] = '0' + VALUE / 10 % 10;
        임시[lengd_VALUE++] = '0' + VALUE % 10;
        if (felt_oppføring < 3) 임시[lengd_VALUE++] = '.';
    }
    임시[lengd_VALUE++] = 0;
    if (용량 < lengd_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int felt_oppføring = 0; felt_oppføring < lengd_VALUE; felt_oppføring++) streng_VALUE[felt_oppføring] = 임시[felt_oppføring];
    return streng_VALUE;
}
