#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *адрес, socklen_t 주소길이) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)адрес, 주소길이, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *данни, size_t 바이트수, int Настройки,
               const struct sockaddr *адрес, socklen_t 주소길이) {
    int искане[2] = {(int)адрес, 주소길이};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)данни, 바이트수, Настройки, (int)искане));
}
ssize_t recvfrom(int 파일서술자, void *данни, size_t 바이트수, int Настройки,
                 struct sockaddr *адрес, socklen_t *주소길이) {
    int искане[2] = {(int)адрес, (int)주소길이};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)данни, 바이트수, Настройки, (int)искане));
}
int getsockname(int 파일서술자, struct sockaddr *адрес, socklen_t *주소길이) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)адрес, (int)주소길이, 0, 0));
}
int setsockopt(int 파일서술자, int слой_стойност, int Настройки_препратка_към_клетка, const void *стойност, socklen_t 값길이) {
    if (слой_стойност != SOL_SOCKET || Настройки_препратка_към_клетка != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!стойност) { errno = EFAULT; return -1; }
    if (값길이 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *час_стойност = стойност;
    if (час_стойност->tv_sec < 0 || час_стойност->tv_sec > 2 || час_стойност->tv_usec < 0 || час_стойност->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = час_стойност->tv_sec * 1000 + (час_стойност->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t стойност) { return (стойност << 8) | (стойност >> 8); }
uint16_t ntohs(uint16_t стойност) { return htons(стойност); }
uint32_t htonl(uint32_t стойност) {
    return (стойност << 24) | ((стойност << 8) & 0xff0000U) | ((стойност >> 8) & 0xff00U) | (стойност >> 24);
}
uint32_t ntohl(uint32_t стойност) { return htonl(стойност); }
int inet_pton(int 주소체계, const char *низ_стойност, void *адрес) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!низ_стойност || !адрес) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int стойност = 0, 자릿수 = 0;
        const char *Стартиране = низ_стойност;
        while (*низ_стойност >= '0' && *низ_стойност <= '9') {
            if (++자릿수 > 3) return 0;
            стойност = стойност * 10 + *низ_стойност++ - '0';
        }
        if (!자릿수 || стойност > 255 || (자릿수 > 1 && *Стартиране == '0')) return 0;
        임시[칸] = стойност;
        if (칸 < 3) { if (*низ_стойност++ != '.') return 0; }
        else if (*низ_стойност) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)адрес)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *адрес, char *низ_стойност, socklen_t капацитет_стойност) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!адрес || !низ_стойност) { errno = EFAULT; return 0; }
    const unsigned char *수 = адрес;
    char 임시[16]; unsigned int 길이 = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int стойност = 수[칸];
        if (стойност >= 100) 임시[길이++] = '0' + стойност / 100;
        if (стойност >= 10) 임시[길이++] = '0' + стойност / 10 % 10;
        임시[길이++] = '0' + стойност % 10;
        if (칸 < 3) 임시[길이++] = '.';
    }
    임시[길이++] = 0;
    if (капацитет_стойност < 길이) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < 길이; 칸++) низ_стойност[칸] = 임시[칸];
    return низ_стойност;
}
