#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *суроға, socklen_t суроға_дарозӣ) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)суроға, суроға_дарозӣ, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *иттилоот, size_t 바이트수, int Танзимот,
               const struct sockaddr *суроға, socklen_t суроға_дарозӣ) {
    int 요청[2] = {(int)суроға, суроға_дарозӣ};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)иттилоот, 바이트수, Танзимот, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *иттилоот, size_t 바이트수, int Танзимот,
                 struct sockaddr *суроға, socklen_t *суроға_дарозӣ) {
    int 요청[2] = {(int)суроға, (int)суроға_дарозӣ};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)иттилоот, 바이트수, Танзимот, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *суроға, socklen_t *суроға_дарозӣ) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)суроға, (int)суроға_дарозӣ, 0, 0));
}
int setsockopt(int 파일서술자, int леер_қимат, int Танзимот_ном, const void *қимат, socklen_t қимат_дарозӣ) {
    if (леер_қимат != SOL_SOCKET || Танзимот_ном != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!қимат) { errno = EFAULT; return -1; }
    if (қимат_дарозӣ != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = қимат;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t қимат) { return (қимат << 8) | (қимат >> 8); }
uint16_t ntohs(uint16_t қимат) { return htons(қимат); }
uint32_t htonl(uint32_t қимат) {
    return (қимат << 24) | ((қимат << 8) & 0xff0000U) | ((қимат >> 8) & 0xff00U) | (қимат >> 24);
}
uint32_t ntohl(uint32_t қимат) { return htonl(қимат); }
int inet_pton(int 주소체계, const char *сатр_қимат_6ca8363c, void *суроға) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!сатр_қимат_6ca8363c || !суроға) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int ковокӣ_ворида = 0; ковокӣ_ворида < 4; ковокӣ_ворида++) {
        int қимат = 0, 자릿수 = 0;
        const char *порча = сатр_қимат_6ca8363c;
        while (*сатр_қимат_6ca8363c >= '0' && *сатр_қимат_6ca8363c <= '9') {
            if (++자릿수 > 3) return 0;
            қимат = қимат * 10 + *сатр_қимат_6ca8363c++ - '0';
        }
        if (!자릿수 || қимат > 255 || (자릿수 > 1 && *порча == '0')) return 0;
        임시[ковокӣ_ворида] = қимат;
        if (ковокӣ_ворида < 3) { if (*сатр_қимат_6ca8363c++ != '.') return 0; }
        else if (*сатр_қимат_6ca8363c) return 0;
    }
    for (int ковокӣ_ворида = 0; ковокӣ_ворида < 4; ковокӣ_ворида++) ((unsigned char *)суроға)[ковокӣ_ворида] = 임시[ковокӣ_ворида];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *суроға, char *сатр_қимат_6ca8363c, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!суроға || !сатр_қимат_6ca8363c) { errno = EFAULT; return 0; }
    const unsigned char *수 = суроға;
    char 임시[16]; unsigned int дарозӣ_қимат = 0;
    for (int ковокӣ_ворида = 0; ковокӣ_ворида < 4; ковокӣ_ворида++) {
        unsigned int қимат = 수[ковокӣ_ворида];
        if (қимат >= 100) 임시[дарозӣ_қимат++] = '0' + қимат / 100;
        if (қимат >= 10) 임시[дарозӣ_қимат++] = '0' + қимат / 10 % 10;
        임시[дарозӣ_қимат++] = '0' + қимат % 10;
        if (ковокӣ_ворида < 3) 임시[дарозӣ_қимат++] = '.';
    }
    임시[дарозӣ_қимат++] = 0;
    if (용량 < дарозӣ_қимат) { errno = ENOSPC; return 0; }
    for (unsigned int ковокӣ_ворида = 0; ковокӣ_ворида < дарозӣ_қимат; ковокӣ_ворида++) сатр_қимат_6ca8363c[ковокӣ_ворида] = 임시[ковокӣ_ворида];
    return сатр_қимат_6ca8363c;
}
