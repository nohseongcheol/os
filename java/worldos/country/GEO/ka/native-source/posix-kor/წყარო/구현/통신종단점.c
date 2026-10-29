#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *მისამართი, socklen_t მისამართი_სიგრძე) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)მისამართი, მისამართი_სიგრძე, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *მონაცემები, size_t 바이트수, int პარამეტრები,
               const struct sockaddr *მისამართი, socklen_t მისამართი_სიგრძე) {
    int 요청[2] = {(int)მისამართი, მისამართი_სიგრძე};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)მონაცემები, 바이트수, პარამეტრები, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *მონაცემები, size_t 바이트수, int პარამეტრები,
                 struct sockaddr *მისამართი, socklen_t *მისამართი_სიგრძე) {
    int 요청[2] = {(int)მისამართი, (int)მისამართი_სიგრძე};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)მონაცემები, 바이트수, პარამეტრები, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *მისამართი, socklen_t *მისამართი_სიგრძე) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)მისამართი, (int)მისამართი_სიგრძე, 0, 0));
}
int setsockopt(int 파일서술자, int შრე_მნიშვნელობა, int პარამეტრები_სახელი, const void *მნიშვნელობა, socklen_t მნიშვნელობა_სიგრძე) {
    if (შრე_მნიშვნელობა != SOL_SOCKET || პარამეტრები_სახელი != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!მნიშვნელობა) { errno = EFAULT; return -1; }
    if (მნიშვნელობა_სიგრძე != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *დრო_მნიშვნელობა = მნიშვნელობა;
    if (დრო_მნიშვნელობა->tv_sec < 0 || დრო_მნიშვნელობა->tv_sec > 2 || დრო_მნიშვნელობა->tv_usec < 0 || დრო_მნიშვნელობა->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = დრო_მნიშვნელობა->tv_sec * 1000 + (დრო_მნიშვნელობა->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t მნიშვნელობა) { return (მნიშვნელობა << 8) | (მნიშვნელობა >> 8); }
uint16_t ntohs(uint16_t მნიშვნელობა) { return htons(მნიშვნელობა); }
uint32_t htonl(uint32_t მნიშვნელობა) {
    return (მნიშვნელობა << 24) | ((მნიშვნელობა << 8) & 0xff0000U) | ((მნიშვნელობა >> 8) & 0xff00U) | (მნიშვნელობა >> 24);
}
uint32_t ntohl(uint32_t მნიშვნელობა) { return htonl(მნიშვნელობა); }
int inet_pton(int 주소체계, const char *სტრიქონი_მნიშვნელობა, void *მისამართი) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!სტრიქონი_მნიშვნელობა || !მისამართი) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int სლოტი_შენატანი = 0; სლოტი_შენატანი < 4; სლოტი_შენატანი++) {
        int მნიშვნელობა = 0, 자릿수 = 0;
        const char *გაშვება = სტრიქონი_მნიშვნელობა;
        while (*სტრიქონი_მნიშვნელობა >= '0' && *სტრიქონი_მნიშვნელობა <= '9') {
            if (++자릿수 > 3) return 0;
            მნიშვნელობა = მნიშვნელობა * 10 + *სტრიქონი_მნიშვნელობა++ - '0';
        }
        if (!자릿수 || მნიშვნელობა > 255 || (자릿수 > 1 && *გაშვება == '0')) return 0;
        임시[სლოტი_შენატანი] = მნიშვნელობა;
        if (სლოტი_შენატანი < 3) { if (*სტრიქონი_მნიშვნელობა++ != '.') return 0; }
        else if (*სტრიქონი_მნიშვნელობა) return 0;
    }
    for (int სლოტი_შენატანი = 0; სლოტი_შენატანი < 4; სლოტი_შენატანი++) ((unsigned char *)მისამართი)[სლოტი_შენატანი] = 임시[სლოტი_შენატანი];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *მისამართი, char *სტრიქონი_მნიშვნელობა, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!მისამართი || !სტრიქონი_მნიშვნელობა) { errno = EFAULT; return 0; }
    const unsigned char *수 = მისამართი;
    char 임시[16]; unsigned int სიგრძე_მნიშვნელობა = 0;
    for (int სლოტი_შენატანი = 0; სლოტი_შენატანი < 4; სლოტი_შენატანი++) {
        unsigned int მნიშვნელობა = 수[სლოტი_შენატანი];
        if (მნიშვნელობა >= 100) 임시[სიგრძე_მნიშვნელობა++] = '0' + მნიშვნელობა / 100;
        if (მნიშვნელობა >= 10) 임시[სიგრძე_მნიშვნელობა++] = '0' + მნიშვნელობა / 10 % 10;
        임시[სიგრძე_მნიშვნელობა++] = '0' + მნიშვნელობა % 10;
        if (სლოტი_შენატანი < 3) 임시[სიგრძე_მნიშვნელობა++] = '.';
    }
    임시[სიგრძე_მნიშვნელობა++] = 0;
    if (용량 < სიგრძე_მნიშვნელობა) { errno = ENOSPC; return 0; }
    for (unsigned int სლოტი_შენატანი = 0; სლოტი_შენატანი < სიგრძე_მნიშვნელობა; სლოტი_შენატანი++) სტრიქონი_მნიშვნელობა[სლოტი_შენატანი] = 임시[სლოტი_შენატანი];
    return სტრიქონი_მნიშვნელობა;
}
