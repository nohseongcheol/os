#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *સરનામું, socklen_t સરનામું_લંબાઈ) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)સરનામું, સરનામું_લંબાઈ, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ડેટા, size_t 바이트수, int સુયોજના,
               const struct sockaddr *સરનામું, socklen_t સરનામું_લંબાઈ) {
    int 요청[2] = {(int)સરનામું, સરનામું_લંબાઈ};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ડેટા, 바이트수, સુયોજના, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ડેટા, size_t 바이트수, int સુયોજના,
                 struct sockaddr *સરનામું, socklen_t *સરનામું_લંબાઈ) {
    int 요청[2] = {(int)સરનામું, (int)સરનામું_લંબાઈ};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ડેટા, 바이트수, સુયોજના, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *સરનામું, socklen_t *સરનામું_લંબાઈ) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)સરનામું, (int)સરનામું_લંબાઈ, 0, 0));
}
int setsockopt(int 파일서술자, int થર_મૂલ્ય, int સેટિંગ્સ_નામ, const void *મૂલ્ય, socklen_t મૂલ્ય_લંબાઈ) {
    if (થર_મૂલ્ય != SOL_SOCKET || સેટિંગ્સ_નામ != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!મૂલ્ય) { errno = EFAULT; return -1; }
    if (મૂલ્ય_લંબાઈ != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *સમય_મૂલ્ય = મૂલ્ય;
    if (સમય_મૂલ્ય->tv_sec < 0 || સમય_મૂલ્ય->tv_sec > 2 || સમય_મૂલ્ય->tv_usec < 0 || સમય_મૂલ્ય->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = સમય_મૂલ્ય->tv_sec * 1000 + (સમય_મૂલ્ય->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t મૂલ્ય) { return (મૂલ્ય << 8) | (મૂલ્ય >> 8); }
uint16_t ntohs(uint16_t મૂલ્ય) { return htons(મૂલ્ય); }
uint32_t htonl(uint32_t મૂલ્ય) {
    return (મૂલ્ય << 24) | ((મૂલ્ય << 8) & 0xff0000U) | ((મૂલ્ય >> 8) & 0xff00U) | (મૂલ્ય >> 24);
}
uint32_t ntohl(uint32_t મૂલ્ય) { return htonl(મૂલ્ય); }
int inet_pton(int 주소체계, const char *સ્ટ્રિંગ_મૂલ્ય, void *સરનામું) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!સ્ટ્રિંગ_મૂલ્ય || !સરનામું) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int સ્લૉટ_પ્રવેશ = 0; સ્લૉટ_પ્રવેશ < 4; સ્લૉટ_પ્રવેશ++) {
        int મૂલ્ય = 0, 자릿수 = 0;
        const char *ચલાવો_2 = સ્ટ્રિંગ_મૂલ્ય;
        while (*સ્ટ્રિંગ_મૂલ્ય >= '0' && *સ્ટ્રિંગ_મૂલ્ય <= '9') {
            if (++자릿수 > 3) return 0;
            મૂલ્ય = મૂલ્ય * 10 + *સ્ટ્રિંગ_મૂલ્ય++ - '0';
        }
        if (!자릿수 || મૂલ્ય > 255 || (자릿수 > 1 && *ચલાવો_2 == '0')) return 0;
        임시[સ્લૉટ_પ્રવેશ] = મૂલ્ય;
        if (સ્લૉટ_પ્રવેશ < 3) { if (*સ્ટ્રિંગ_મૂલ્ય++ != '.') return 0; }
        else if (*સ્ટ્રિંગ_મૂલ્ય) return 0;
    }
    for (int સ્લૉટ_પ્રવેશ = 0; સ્લૉટ_પ્રવેશ < 4; સ્લૉટ_પ્રવેશ++) ((unsigned char *)સરનામું)[સ્લૉટ_પ્રવેશ] = 임시[સ્લૉટ_પ્રવેશ];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *સરનામું, char *સ્ટ્રિંગ_મૂલ્ય, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!સરનામું || !સ્ટ્રિંગ_મૂલ્ય) { errno = EFAULT; return 0; }
    const unsigned char *수 = સરનામું;
    char 임시[16]; unsigned int લંબાઈ_મૂલ્ય = 0;
    for (int સ્લૉટ_પ્રવેશ = 0; સ્લૉટ_પ્રવેશ < 4; સ્લૉટ_પ્રવેશ++) {
        unsigned int મૂલ્ય = 수[સ્લૉટ_પ્રવેશ];
        if (મૂલ્ય >= 100) 임시[લંબાઈ_મૂલ્ય++] = '0' + મૂલ્ય / 100;
        if (મૂલ્ય >= 10) 임시[લંબાઈ_મૂલ્ય++] = '0' + મૂલ્ય / 10 % 10;
        임시[લંબાઈ_મૂલ્ય++] = '0' + મૂલ્ય % 10;
        if (સ્લૉટ_પ્રવેશ < 3) 임시[લંબાઈ_મૂલ્ય++] = '.';
    }
    임시[લંબાઈ_મૂલ્ય++] = 0;
    if (용량 < લંબાઈ_મૂલ્ય) { errno = ENOSPC; return 0; }
    for (unsigned int સ્લૉટ_પ્રવેશ = 0; સ્લૉટ_પ્રવેશ < લંબાઈ_મૂલ્ય; સ્લૉટ_પ્રવેશ++) સ્ટ્રિંગ_મૂલ્ય[સ્લૉટ_પ્રવેશ] = 임시[સ્લૉટ_પ્રવેશ];
    return સ્ટ્રિંગ_મૂલ્ય;
}
