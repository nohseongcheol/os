#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *پته, socklen_t پته_اوږدوالى) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)پته, پته_اوږدوالى, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *اومتوک, size_t 바이트수, int امستنې,
               const struct sockaddr *پته, socklen_t پته_اوږدوالى) {
    int 요청[2] = {(int)پته, پته_اوږدوالى};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)اومتوک, 바이트수, امستنې, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *اومتوک, size_t 바이트수, int امستنې,
                 struct sockaddr *پته, socklen_t *پته_اوږدوالى) {
    int 요청[2] = {(int)پته, (int)پته_اوږدوالى};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)اومتوک, 바이트수, امستنې, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *پته, socklen_t *پته_اوږدوالى) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)پته, (int)پته_اوږدوالى, 0, 0));
}
int setsockopt(int 파일서술자, int لهر_ارزښت, int 설정이름, const void *ارزښت, socklen_t ارزښت_اوږدوالى) {
    if (لهر_ارزښت != SOL_SOCKET || 설정이름 != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ارزښت) { errno = EFAULT; return -1; }
    if (ارزښت_اوږدوالى != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = ارزښت;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ارزښت) { return (ارزښت << 8) | (ارزښت >> 8); }
uint16_t ntohs(uint16_t ارزښت) { return htons(ارزښت); }
uint32_t htonl(uint32_t ارزښت) {
    return (ارزښت << 24) | ((ارزښت << 8) & 0xff0000U) | ((ارزښت >> 8) & 0xff00U) | (ارزښت >> 24);
}
uint32_t ntohl(uint32_t ارزښت) { return htonl(ارزښت); }
int inet_pton(int 주소체계, const char *مزى_ارزښت_6ca8363c, void *پته) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!مزى_ارزښت_6ca8363c || !پته) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int ارزښت = 0, 자릿수 = 0;
        const char *ځغلول = مزى_ارزښت_6ca8363c;
        while (*مزى_ارزښت_6ca8363c >= '0' && *مزى_ارزښت_6ca8363c <= '9') {
            if (++자릿수 > 3) return 0;
            ارزښت = ارزښت * 10 + *مزى_ارزښت_6ca8363c++ - '0';
        }
        if (!자릿수 || ارزښت > 255 || (자릿수 > 1 && *ځغلول == '0')) return 0;
        임시[칸] = ارزښت;
        if (칸 < 3) { if (*مزى_ارزښت_6ca8363c++ != '.') return 0; }
        else if (*مزى_ارزښت_6ca8363c) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)پته)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *پته, char *مزى_ارزښت_6ca8363c, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!پته || !مزى_ارزښت_6ca8363c) { errno = EFAULT; return 0; }
    const unsigned char *수 = پته;
    char 임시[16]; unsigned int اوږدوالى_ارزښت = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int ارزښت = 수[칸];
        if (ارزښت >= 100) 임시[اوږدوالى_ارزښت++] = '0' + ارزښت / 100;
        if (ارزښت >= 10) 임시[اوږدوالى_ارزښت++] = '0' + ارزښت / 10 % 10;
        임시[اوږدوالى_ارزښت++] = '0' + ارزښت % 10;
        if (칸 < 3) 임시[اوږدوالى_ارزښت++] = '.';
    }
    임시[اوږدوالى_ارزښت++] = 0;
    if (용량 < اوږدوالى_ارزښت) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < اوږدوالى_ارزښت; 칸++) مزى_ارزښت_6ca8363c[칸] = 임시[칸];
    return مزى_ارزښت_6ca8363c;
}
