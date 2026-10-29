#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *адреса, socklen_t адреса_дужина) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)адреса, адреса_дужина, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *подаци, size_t 바이트수, int Подешавања,
               const struct sockaddr *адреса, socklen_t адреса_дужина) {
    int 요청[2] = {(int)адреса, адреса_дужина};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)подаци, 바이트수, Подешавања, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *подаци, size_t 바이트수, int Подешавања,
                 struct sockaddr *адреса, socklen_t *адреса_дужина) {
    int 요청[2] = {(int)адреса, (int)адреса_дужина};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)подаци, 바이트수, Подешавања, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *адреса, socklen_t *адреса_дужина) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)адреса, (int)адреса_дужина, 0, 0));
}
int setsockopt(int 파일서술자, int слој_вриједност, int Подешавања_назив, const void *вриједност, socklen_t вриједност_дужина) {
    if (слој_вриједност != SOL_SOCKET || Подешавања_назив != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!вриједност) { errno = EFAULT; return -1; }
    if (вриједност_дужина != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = вриједност;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t вриједност) { return (вриједност << 8) | (вриједност >> 8); }
uint16_t ntohs(uint16_t вриједност) { return htons(вриједност); }
uint32_t htonl(uint32_t вриједност) {
    return (вриједност << 24) | ((вриједност << 8) & 0xff0000U) | ((вриједност >> 8) & 0xff00U) | (вриједност >> 24);
}
uint32_t ntohl(uint32_t вриједност) { return htonl(вриједност); }
int inet_pton(int 주소체계, const char *стринг_вриједност, void *адреса) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!стринг_вриједност || !адреса) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int вриједност = 0, 자릿수 = 0;
        const char *시작 = стринг_вриједност;
        while (*стринг_вриједност >= '0' && *стринг_вриједност <= '9') {
            if (++자릿수 > 3) return 0;
            вриједност = вриједност * 10 + *стринг_вриједност++ - '0';
        }
        if (!자릿수 || вриједност > 255 || (자릿수 > 1 && *시작 == '0')) return 0;
        임시[칸] = вриједност;
        if (칸 < 3) { if (*стринг_вриједност++ != '.') return 0; }
        else if (*стринг_вриједност) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)адреса)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *адреса, char *стринг_вриједност, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!адреса || !стринг_вриједност) { errno = EFAULT; return 0; }
    const unsigned char *수 = адреса;
    char 임시[16]; unsigned int дужина_вриједност = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int вриједност = 수[칸];
        if (вриједност >= 100) 임시[дужина_вриједност++] = '0' + вриједност / 100;
        if (вриједност >= 10) 임시[дужина_вриједност++] = '0' + вриједност / 10 % 10;
        임시[дужина_вриједност++] = '0' + вриједност % 10;
        if (칸 < 3) 임시[дужина_вриједност++] = '.';
    }
    임시[дужина_вриједност++] = 0;
    if (용량 < дужина_вриједност) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < дужина_вриједност; 칸++) стринг_вриједност[칸] = 임시[칸];
    return стринг_вриједност;
}
