#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *хаяг, socklen_t хаяг_урт) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)хаяг, хаяг_урт, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *өгөгдөл, size_t 바이트수, int Тохиргоо,
               const struct sockaddr *хаяг, socklen_t хаяг_урт) {
    int 요청[2] = {(int)хаяг, хаяг_урт};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)өгөгдөл, 바이트수, Тохиргоо, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *өгөгдөл, size_t 바이트수, int Тохиргоо,
                 struct sockaddr *хаяг, socklen_t *хаяг_урт) {
    int 요청[2] = {(int)хаяг, (int)хаяг_урт};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)өгөгдөл, 바이트수, Тохиргоо, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *хаяг, socklen_t *хаяг_урт) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)хаяг, (int)хаяг_урт, 0, 0));
}
int setsockopt(int 파일서술자, int үе_шат_утга, int Тохиргоо_нэр, const void *утга, socklen_t утга_урт) {
    if (үе_шат_утга != SOL_SOCKET || Тохиргоо_нэр != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!утга) { errno = EFAULT; return -1; }
    if (утга_урт != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = утга;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t утга) { return (утга << 8) | (утга >> 8); }
uint16_t ntohs(uint16_t утга) { return htons(утга); }
uint32_t htonl(uint32_t утга) {
    return (утга << 24) | ((утга << 8) & 0xff0000U) | ((утга >> 8) & 0xff00U) | (утга >> 24);
}
uint32_t ntohl(uint32_t утга) { return htonl(утга); }
int inet_pton(int 주소체계, const char *мөр_утга_6ca8363c, void *хаяг) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!мөр_утга_6ca8363c || !хаяг) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int зай_оролт = 0; зай_оролт < 4; зай_оролт++) {
        int утга = 0, 자릿수 = 0;
        const char *Ажиллуулах = мөр_утга_6ca8363c;
        while (*мөр_утга_6ca8363c >= '0' && *мөр_утга_6ca8363c <= '9') {
            if (++자릿수 > 3) return 0;
            утга = утга * 10 + *мөр_утга_6ca8363c++ - '0';
        }
        if (!자릿수 || утга > 255 || (자릿수 > 1 && *Ажиллуулах == '0')) return 0;
        임시[зай_оролт] = утга;
        if (зай_оролт < 3) { if (*мөр_утга_6ca8363c++ != '.') return 0; }
        else if (*мөр_утга_6ca8363c) return 0;
    }
    for (int зай_оролт = 0; зай_оролт < 4; зай_оролт++) ((unsigned char *)хаяг)[зай_оролт] = 임시[зай_оролт];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *хаяг, char *мөр_утга_6ca8363c, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!хаяг || !мөр_утга_6ca8363c) { errno = EFAULT; return 0; }
    const unsigned char *수 = хаяг;
    char 임시[16]; unsigned int урт_утга = 0;
    for (int зай_оролт = 0; зай_оролт < 4; зай_оролт++) {
        unsigned int утга = 수[зай_оролт];
        if (утга >= 100) 임시[урт_утга++] = '0' + утга / 100;
        if (утга >= 10) 임시[урт_утга++] = '0' + утга / 10 % 10;
        임시[урт_утга++] = '0' + утга % 10;
        if (зай_оролт < 3) 임시[урт_утга++] = '.';
    }
    임시[урт_утга++] = 0;
    if (용량 < урт_утга) { errno = ENOSPC; return 0; }
    for (unsigned int зай_оролт = 0; зай_оролт < урт_утга; зай_оролт++) мөр_утга_6ca8363c[зай_оролт] = 임시[зай_оролт];
    return мөр_утга_6ca8363c;
}
