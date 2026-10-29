#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int mál_númer) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, mál_númer, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *slóð, socklen_t slóð_lengd_6e50507f) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)slóð, slóð_lengd_6e50507f, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *gögn, size_t bæti_COUNT, int Stillingar,
               const struct sockaddr *slóð, socklen_t slóð_lengd_6e50507f) {
    int 요청[2] = {(int)slóð, slóð_lengd_6e50507f};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)gögn, bæti_COUNT, Stillingar, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *gögn, size_t bæti_COUNT, int Stillingar,
                 struct sockaddr *slóð, socklen_t *slóð_lengd_6e50507f) {
    int 요청[2] = {(int)slóð, (int)slóð_lengd_6e50507f};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)gögn, bæti_COUNT, Stillingar, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *slóð, socklen_t *slóð_lengd_6e50507f) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)slóð, (int)slóð_lengd_6e50507f, 0, 0));
}
int setsockopt(int 파일서술자, int lag_VALUE, int Stillingar_heiti, const void *VALUE, socklen_t VALUE_lengd) {
    if (lag_VALUE != SOL_SOCKET || Stillingar_heiti != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
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
int inet_pton(int 주소체계, const char *strengur_VALUE, void *slóð) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!strengur_VALUE || !slóð) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int rauf_færsla = 0; rauf_færsla < 4; rauf_færsla++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Keyra_2 = strengur_VALUE;
        while (*strengur_VALUE >= '0' && *strengur_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *strengur_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Keyra_2 == '0')) return 0;
        임시[rauf_færsla] = VALUE;
        if (rauf_færsla < 3) { if (*strengur_VALUE++ != '.') return 0; }
        else if (*strengur_VALUE) return 0;
    }
    for (int rauf_færsla = 0; rauf_færsla < 4; rauf_færsla++) ((unsigned char *)slóð)[rauf_færsla] = 임시[rauf_færsla];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *slóð, char *strengur_VALUE, socklen_t afkastageta_VALUE) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!slóð || !strengur_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *númer = slóð;
    char 임시[16]; unsigned int lengd_VALUE = 0;
    for (int rauf_færsla = 0; rauf_færsla < 4; rauf_færsla++) {
        unsigned int VALUE = númer[rauf_færsla];
        if (VALUE >= 100) 임시[lengd_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[lengd_VALUE++] = '0' + VALUE / 10 % 10;
        임시[lengd_VALUE++] = '0' + VALUE % 10;
        if (rauf_færsla < 3) 임시[lengd_VALUE++] = '.';
    }
    임시[lengd_VALUE++] = 0;
    if (afkastageta_VALUE < lengd_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int rauf_færsla = 0; rauf_færsla < lengd_VALUE; rauf_færsla++) strengur_VALUE[rauf_færsla] = 임시[rauf_færsla];
    return strengur_VALUE;
}
