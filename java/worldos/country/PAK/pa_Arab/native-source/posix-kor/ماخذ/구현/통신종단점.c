#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *پتا, socklen_t پتا_لمبائی) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)پتا, پتا_لمبائی, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *کوائف, size_t 바이트수, int سیٹنگاں,
               const struct sockaddr *پتا, socklen_t پتا_لمبائی) {
    int 요청[2] = {(int)پتا, پتا_لمبائی};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)کوائف, 바이트수, سیٹنگاں, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *کوائف, size_t 바이트수, int سیٹنگاں,
                 struct sockaddr *پتا, socklen_t *پتا_لمبائی) {
    int 요청[2] = {(int)پتا, (int)پتا_لمبائی};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)کوائف, 바이트수, سیٹنگاں, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *پتا, socklen_t *پتا_لمبائی) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)پتا, (int)پتا_لمبائی, 0, 0));
}
int setsockopt(int 파일서술자, int پرت_قدر, int سیٹنگاں_ناں, const void *قدر, socklen_t قدر_لمبائی) {
    if (پرت_قدر != SOL_SOCKET || سیٹنگاں_ناں != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!قدر) { errno = EFAULT; return -1; }
    if (قدر_لمبائی != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = قدر;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t قدر) { return (قدر << 8) | (قدر >> 8); }
uint16_t ntohs(uint16_t قدر) { return htons(قدر); }
uint32_t htonl(uint32_t قدر) {
    return (قدر << 24) | ((قدر << 8) & 0xff0000U) | ((قدر >> 8) & 0xff00U) | (قدر >> 24);
}
uint32_t ntohl(uint32_t قدر) { return htonl(قدر); }
int inet_pton(int 주소체계, const char *سٹرنگ_قدر, void *پتا) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!سٹرنگ_قدر || !پتا) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int سلاٹ_داخلہ = 0; سلاٹ_داخلہ < 4; سلاٹ_داخلہ++) {
        int قدر = 0, 자릿수 = 0;
        const char *چلاؤ = سٹرنگ_قدر;
        while (*سٹرنگ_قدر >= '0' && *سٹرنگ_قدر <= '9') {
            if (++자릿수 > 3) return 0;
            قدر = قدر * 10 + *سٹرنگ_قدر++ - '0';
        }
        if (!자릿수 || قدر > 255 || (자릿수 > 1 && *چلاؤ == '0')) return 0;
        임시[سلاٹ_داخلہ] = قدر;
        if (سلاٹ_داخلہ < 3) { if (*سٹرنگ_قدر++ != '.') return 0; }
        else if (*سٹرنگ_قدر) return 0;
    }
    for (int سلاٹ_داخلہ = 0; سلاٹ_داخلہ < 4; سلاٹ_داخلہ++) ((unsigned char *)پتا)[سلاٹ_داخلہ] = 임시[سلاٹ_داخلہ];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *پتا, char *سٹرنگ_قدر, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!پتا || !سٹرنگ_قدر) { errno = EFAULT; return 0; }
    const unsigned char *수 = پتا;
    char 임시[16]; unsigned int لمبائی_قدر = 0;
    for (int سلاٹ_داخلہ = 0; سلاٹ_داخلہ < 4; سلاٹ_داخلہ++) {
        unsigned int قدر = 수[سلاٹ_داخلہ];
        if (قدر >= 100) 임시[لمبائی_قدر++] = '0' + قدر / 100;
        if (قدر >= 10) 임시[لمبائی_قدر++] = '0' + قدر / 10 % 10;
        임시[لمبائی_قدر++] = '0' + قدر % 10;
        if (سلاٹ_داخلہ < 3) 임시[لمبائی_قدر++] = '.';
    }
    임시[لمبائی_قدر++] = 0;
    if (용량 < لمبائی_قدر) { errno = ENOSPC; return 0; }
    for (unsigned int سلاٹ_داخلہ = 0; سلاٹ_داخلہ < لمبائی_قدر; سلاٹ_داخلہ++) سٹرنگ_قدر[سلاٹ_داخلہ] = 임시[سلاٹ_داخلہ];
    return سٹرنگ_قدر;
}
