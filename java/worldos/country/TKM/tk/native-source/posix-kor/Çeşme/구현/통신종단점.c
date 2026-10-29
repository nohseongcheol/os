#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *salgy, socklen_t salgy_dowamlylyk) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)salgy, salgy_dowamlylyk, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *maglumat, size_t 바이트수, int Düzümler,
               const struct sockaddr *salgy, socklen_t salgy_dowamlylyk) {
    int 요청[2] = {(int)salgy, salgy_dowamlylyk};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)maglumat, 바이트수, Düzümler, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *maglumat, size_t 바이트수, int Düzümler,
                 struct sockaddr *salgy, socklen_t *salgy_dowamlylyk) {
    int 요청[2] = {(int)salgy, (int)salgy_dowamlylyk};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)maglumat, 바이트수, Düzümler, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *salgy, socklen_t *salgy_dowamlylyk) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)salgy, (int)salgy_dowamlylyk, 0, 0));
}
int setsockopt(int 파일서술자, int dereje_baha, int Sazlamalar_at, const void *baha, socklen_t baha_dowamlylyk) {
    if (dereje_baha != SOL_SOCKET || Sazlamalar_at != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!baha) { errno = EFAULT; return -1; }
    if (baha_dowamlylyk != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = baha;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t baha) { return (baha << 8) | (baha >> 8); }
uint16_t ntohs(uint16_t baha) { return htons(baha); }
uint32_t htonl(uint32_t baha) {
    return (baha << 24) | ((baha << 8) & 0xff0000U) | ((baha >> 8) & 0xff00U) | (baha >> 24);
}
uint32_t ntohl(uint32_t baha) { return htonl(baha); }
int inet_pton(int 주소체계, const char *setir_baha_6ca8363c, void *salgy) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!setir_baha_6ca8363c || !salgy) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int ýer_girizmeklik = 0; ýer_girizmeklik < 4; ýer_girizmeklik++) {
        int baha = 0, 자릿수 = 0;
        const char *Bitir = setir_baha_6ca8363c;
        while (*setir_baha_6ca8363c >= '0' && *setir_baha_6ca8363c <= '9') {
            if (++자릿수 > 3) return 0;
            baha = baha * 10 + *setir_baha_6ca8363c++ - '0';
        }
        if (!자릿수 || baha > 255 || (자릿수 > 1 && *Bitir == '0')) return 0;
        임시[ýer_girizmeklik] = baha;
        if (ýer_girizmeklik < 3) { if (*setir_baha_6ca8363c++ != '.') return 0; }
        else if (*setir_baha_6ca8363c) return 0;
    }
    for (int ýer_girizmeklik = 0; ýer_girizmeklik < 4; ýer_girizmeklik++) ((unsigned char *)salgy)[ýer_girizmeklik] = 임시[ýer_girizmeklik];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *salgy, char *setir_baha_6ca8363c, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!salgy || !setir_baha_6ca8363c) { errno = EFAULT; return 0; }
    const unsigned char *수 = salgy;
    char 임시[16]; unsigned int dowamlylyk_baha = 0;
    for (int ýer_girizmeklik = 0; ýer_girizmeklik < 4; ýer_girizmeklik++) {
        unsigned int baha = 수[ýer_girizmeklik];
        if (baha >= 100) 임시[dowamlylyk_baha++] = '0' + baha / 100;
        if (baha >= 10) 임시[dowamlylyk_baha++] = '0' + baha / 10 % 10;
        임시[dowamlylyk_baha++] = '0' + baha % 10;
        if (ýer_girizmeklik < 3) 임시[dowamlylyk_baha++] = '.';
    }
    임시[dowamlylyk_baha++] = 0;
    if (용량 < dowamlylyk_baha) { errno = ENOSPC; return 0; }
    for (unsigned int ýer_girizmeklik = 0; ýer_girizmeklik < dowamlylyk_baha; ýer_girizmeklik++) setir_baha_6ca8363c[ýer_girizmeklik] = 임시[ýer_girizmeklik];
    return setir_baha_6ca8363c;
}
