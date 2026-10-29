#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *پتہ, socklen_t پتہ_لمبا_ئی) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)پتہ, پتہ_لمبا_ئی, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *کوائف, size_t 바이트수, int ترتیبات,
               const struct sockaddr *پتہ, socklen_t پتہ_لمبا_ئی) {
    int 요청[2] = {(int)پتہ, پتہ_لمبا_ئی};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)کوائف, 바이트수, ترتیبات, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *کوائف, size_t 바이트수, int ترتیبات,
                 struct sockaddr *پتہ, socklen_t *پتہ_لمبا_ئی) {
    int 요청[2] = {(int)پتہ, (int)پتہ_لمبا_ئی};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)کوائف, 바이트수, ترتیبات, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *پتہ, socklen_t *پتہ_لمبا_ئی) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)پتہ, (int)پتہ_لمبا_ئی, 0, 0));
}
int setsockopt(int 파일서술자, int پرت_قدر, int سیٹنگز_نام, const void *قدر, socklen_t قدر_لمبا_ئی) {
    if (پرت_قدر != SOL_SOCKET || سیٹنگز_نام != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!قدر) { errno = EFAULT; return -1; }
    if (قدر_لمبا_ئی != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *وقت_قدر = قدر;
    if (وقت_قدر->tv_sec < 0 || وقت_قدر->tv_sec > 2 || وقت_قدر->tv_usec < 0 || وقت_قدر->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = وقت_قدر->tv_sec * 1000 + (وقت_قدر->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t قدر) { return (قدر << 8) | (قدر >> 8); }
uint16_t ntohs(uint16_t قدر) { return htons(قدر); }
uint32_t htonl(uint32_t قدر) {
    return (قدر << 24) | ((قدر << 8) & 0xff0000U) | ((قدر >> 8) & 0xff00U) | (قدر >> 24);
}
uint32_t ntohl(uint32_t قدر) { return htonl(قدر); }
int inet_pton(int 주소체계, const char *سلک_قدر, void *پتہ) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!سلک_قدر || !پتہ) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int سلاٹ_اندراج = 0; سلاٹ_اندراج < 4; سلاٹ_اندراج++) {
        int قدر = 0, 자릿수 = 0;
        const char *چلائیں = سلک_قدر;
        while (*سلک_قدر >= '0' && *سلک_قدر <= '9') {
            if (++자릿수 > 3) return 0;
            قدر = قدر * 10 + *سلک_قدر++ - '0';
        }
        if (!자릿수 || قدر > 255 || (자릿수 > 1 && *چلائیں == '0')) return 0;
        임시[سلاٹ_اندراج] = قدر;
        if (سلاٹ_اندراج < 3) { if (*سلک_قدر++ != '.') return 0; }
        else if (*سلک_قدر) return 0;
    }
    for (int سلاٹ_اندراج = 0; سلاٹ_اندراج < 4; سلاٹ_اندراج++) ((unsigned char *)پتہ)[سلاٹ_اندراج] = 임시[سلاٹ_اندراج];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *پتہ, char *سلک_قدر, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!پتہ || !سلک_قدر) { errno = EFAULT; return 0; }
    const unsigned char *수 = پتہ;
    char 임시[16]; unsigned int لمبا_ئی_قدر = 0;
    for (int سلاٹ_اندراج = 0; سلاٹ_اندراج < 4; سلاٹ_اندراج++) {
        unsigned int قدر = 수[سلاٹ_اندراج];
        if (قدر >= 100) 임시[لمبا_ئی_قدر++] = '0' + قدر / 100;
        if (قدر >= 10) 임시[لمبا_ئی_قدر++] = '0' + قدر / 10 % 10;
        임시[لمبا_ئی_قدر++] = '0' + قدر % 10;
        if (سلاٹ_اندراج < 3) 임시[لمبا_ئی_قدر++] = '.';
    }
    임시[لمبا_ئی_قدر++] = 0;
    if (용량 < لمبا_ئی_قدر) { errno = ENOSPC; return 0; }
    for (unsigned int سلاٹ_اندراج = 0; سلاٹ_اندراج < لمبا_ئی_قدر; سلاٹ_اندراج++) سلک_قدر[سلاٹ_اندراج] = 임시[سلاٹ_اندراج];
    return سلک_قدر;
}
