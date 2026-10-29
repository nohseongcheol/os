#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *адреса, socklen_t адреса_дужина) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)адреса, адреса_дужина, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *подаци, size_t 바이트수, int Поставке,
               const struct sockaddr *адреса, socklen_t адреса_дужина) {
    int захтев[2] = {(int)адреса, адреса_дужина};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)подаци, 바이트수, Поставке, (int)захтев));
}
ssize_t recvfrom(int 파일서술자, void *подаци, size_t 바이트수, int Поставке,
                 struct sockaddr *адреса, socklen_t *адреса_дужина) {
    int захтев[2] = {(int)адреса, (int)адреса_дужина};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)подаци, 바이트수, Поставке, (int)захтев));
}
int getsockname(int 파일서술자, struct sockaddr *адреса, socklen_t *адреса_дужина) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)адреса, (int)адреса_дужина, 0, 0));
}
int setsockopt(int 파일서술자, int слој_вриједност, int Поставке_име, const void *вриједност, socklen_t вриједност_дужина) {
    if (слој_вриједност != SOL_SOCKET || Поставке_име != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!вриједност) { errno = EFAULT; return -1; }
    if (вриједност_дужина != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *време_вриједност = вриједност;
    if (време_вриједност->tv_sec < 0 || време_вриједност->tv_sec > 2 || време_вриједност->tv_usec < 0 || време_вриједност->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = време_вриједност->tv_sec * 1000 + (време_вриједност->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t вриједност) { return (вриједност << 8) | (вриједност >> 8); }
uint16_t ntohs(uint16_t вриједност) { return htons(вриједност); }
uint32_t htonl(uint32_t вриједност) {
    return (вриједност << 24) | ((вриједност << 8) & 0xff0000U) | ((вриједност >> 8) & 0xff00U) | (вриједност >> 24);
}
uint32_t ntohl(uint32_t вриједност) { return htonl(вриједност); }
int inet_pton(int 주소체계, const char *ниска_вриједност, void *адреса) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ниска_вриједност || !адреса) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int простор_за_унос_унос = 0; простор_за_унос_унос < 4; простор_за_унос_унос++) {
        int вриједност = 0, 자릿수 = 0;
        const char *Покрени = ниска_вриједност;
        while (*ниска_вриједност >= '0' && *ниска_вриједност <= '9') {
            if (++자릿수 > 3) return 0;
            вриједност = вриједност * 10 + *ниска_вриједност++ - '0';
        }
        if (!자릿수 || вриједност > 255 || (자릿수 > 1 && *Покрени == '0')) return 0;
        임시[простор_за_унос_унос] = вриједност;
        if (простор_за_унос_унос < 3) { if (*ниска_вриједност++ != '.') return 0; }
        else if (*ниска_вриједност) return 0;
    }
    for (int простор_за_унос_унос = 0; простор_за_унос_унос < 4; простор_за_унос_унос++) ((unsigned char *)адреса)[простор_за_унос_унос] = 임시[простор_за_унос_унос];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *адреса, char *ниска_вриједност, socklen_t капацитет_вриједност) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!адреса || !ниска_вриједност) { errno = EFAULT; return 0; }
    const unsigned char *수 = адреса;
    char 임시[16]; unsigned int дужина_вриједност = 0;
    for (int простор_за_унос_унос = 0; простор_за_унос_унос < 4; простор_за_унос_унос++) {
        unsigned int вриједност = 수[простор_за_унос_унос];
        if (вриједност >= 100) 임시[дужина_вриједност++] = '0' + вриједност / 100;
        if (вриједност >= 10) 임시[дужина_вриједност++] = '0' + вриједност / 10 % 10;
        임시[дужина_вриједност++] = '0' + вриједност % 10;
        if (простор_за_унос_унос < 3) 임시[дужина_вриједност++] = '.';
    }
    임시[дужина_вриједност++] = 0;
    if (капацитет_вриједност < дужина_вриједност) { errno = ENOSPC; return 0; }
    for (unsigned int простор_за_унос_унос = 0; простор_за_унос_унос < дужина_вриједност; простор_за_унос_унос++) ниска_вриједност[простор_за_унос_унос] = 임시[простор_за_унос_унос];
    return ниска_вриједност;
}
