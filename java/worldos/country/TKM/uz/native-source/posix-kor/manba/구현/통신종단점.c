#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *manzil, socklen_t manzil_uzunlik) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)manzil, manzil_uzunlik, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ma_lumotlar, size_t bayt_COUNT, int Moslamalar,
               const struct sockaddr *manzil, socklen_t manzil_uzunlik) {
    int 요청[2] = {(int)manzil, manzil_uzunlik};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ma_lumotlar, bayt_COUNT, Moslamalar, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ma_lumotlar, size_t bayt_COUNT, int Moslamalar,
                 struct sockaddr *manzil, socklen_t *manzil_uzunlik) {
    int 요청[2] = {(int)manzil, (int)manzil_uzunlik};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ma_lumotlar, bayt_COUNT, Moslamalar, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *manzil, socklen_t *manzil_uzunlik) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)manzil, (int)manzil_uzunlik, 0, 0));
}
int setsockopt(int 파일서술자, int qatlam_VALUE, int Sozlamalar_nom, const void *VALUE, socklen_t VALUE_uzunlik) {
    if (qatlam_VALUE != SOL_SOCKET || Sozlamalar_nom != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_uzunlik != sizeof(struct timeval)) { errno = EINVAL; return -1; }
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
int inet_pton(int 주소체계, const char *satr_VALUE, void *manzil) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!satr_VALUE || !manzil) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int in_kiritish = 0; in_kiritish < 4; in_kiritish++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Bajarish = satr_VALUE;
        while (*satr_VALUE >= '0' && *satr_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *satr_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Bajarish == '0')) return 0;
        임시[in_kiritish] = VALUE;
        if (in_kiritish < 3) { if (*satr_VALUE++ != '.') return 0; }
        else if (*satr_VALUE) return 0;
    }
    for (int in_kiritish = 0; in_kiritish < 4; in_kiritish++) ((unsigned char *)manzil)[in_kiritish] = 임시[in_kiritish];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *manzil, char *satr_VALUE, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!manzil || !satr_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = manzil;
    char 임시[16]; unsigned int uzunlik_VALUE = 0;
    for (int in_kiritish = 0; in_kiritish < 4; in_kiritish++) {
        unsigned int VALUE = 수[in_kiritish];
        if (VALUE >= 100) 임시[uzunlik_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[uzunlik_VALUE++] = '0' + VALUE / 10 % 10;
        임시[uzunlik_VALUE++] = '0' + VALUE % 10;
        if (in_kiritish < 3) 임시[uzunlik_VALUE++] = '.';
    }
    임시[uzunlik_VALUE++] = 0;
    if (용량 < uzunlik_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int in_kiritish = 0; in_kiritish < uzunlik_VALUE; in_kiritish++) satr_VALUE[in_kiritish] = 임시[in_kiritish];
    return satr_VALUE;
}
