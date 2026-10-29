#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *adres, socklen_t adres_lengte) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)adres, adres_lengte, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t greep_COUNT, int Instellings,
               const struct sockaddr *adres, socklen_t adres_lengte) {
    int 요청[2] = {(int)adres, adres_lengte};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, greep_COUNT, Instellings, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t greep_COUNT, int Instellings,
                 struct sockaddr *adres, socklen_t *adres_lengte) {
    int 요청[2] = {(int)adres, (int)adres_lengte};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, greep_COUNT, Instellings, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *adres, socklen_t *adres_lengte) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)adres, (int)adres_lengte, 0, 0));
}
int setsockopt(int 파일서술자, int laag_VALUE, int Instellings_naam, const void *VALUE, socklen_t VALUE_lengte) {
    if (laag_VALUE != SOL_SOCKET || Instellings_naam != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_lengte != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *tyd_VALUE = VALUE;
    if (tyd_VALUE->tv_sec < 0 || tyd_VALUE->tv_sec > 2 || tyd_VALUE->tv_usec < 0 || tyd_VALUE->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = tyd_VALUE->tv_sec * 1000 + (tyd_VALUE->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VALUE) { return (VALUE << 8) | (VALUE >> 8); }
uint16_t ntohs(uint16_t VALUE) { return htons(VALUE); }
uint32_t htonl(uint32_t VALUE) {
    return (VALUE << 24) | ((VALUE << 8) & 0xff0000U) | ((VALUE >> 8) & 0xff00U) | (VALUE >> 24);
}
uint32_t ntohl(uint32_t VALUE) { return htonl(VALUE); }
int inet_pton(int 주소체계, const char *string_VALUE, void *adres) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!string_VALUE || !adres) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int gleuf_inskrywing = 0; gleuf_inskrywing < 4; gleuf_inskrywing++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Loop = string_VALUE;
        while (*string_VALUE >= '0' && *string_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *string_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Loop == '0')) return 0;
        임시[gleuf_inskrywing] = VALUE;
        if (gleuf_inskrywing < 3) { if (*string_VALUE++ != '.') return 0; }
        else if (*string_VALUE) return 0;
    }
    for (int gleuf_inskrywing = 0; gleuf_inskrywing < 4; gleuf_inskrywing++) ((unsigned char *)adres)[gleuf_inskrywing] = 임시[gleuf_inskrywing];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *adres, char *string_VALUE, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!adres || !string_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = adres;
    char 임시[16]; unsigned int lengte_VALUE = 0;
    for (int gleuf_inskrywing = 0; gleuf_inskrywing < 4; gleuf_inskrywing++) {
        unsigned int VALUE = 수[gleuf_inskrywing];
        if (VALUE >= 100) 임시[lengte_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[lengte_VALUE++] = '0' + VALUE / 10 % 10;
        임시[lengte_VALUE++] = '0' + VALUE % 10;
        if (gleuf_inskrywing < 3) 임시[lengte_VALUE++] = '.';
    }
    임시[lengte_VALUE++] = 0;
    if (용량 < lengte_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int gleuf_inskrywing = 0; gleuf_inskrywing < lengte_VALUE; gleuf_inskrywing++) string_VALUE[gleuf_inskrywing] = 임시[gleuf_inskrywing];
    return string_VALUE;
}
