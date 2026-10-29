#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *adresa, socklen_t adresa_lungime) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)adresa, adresa_lungime, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *date, size_t byte_COUNT, int Setări,
               const struct sockaddr *adresa, socklen_t adresa_lungime) {
    int cerere[2] = {(int)adresa, adresa_lungime};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)date, byte_COUNT, Setări, (int)cerere));
}
ssize_t recvfrom(int 파일서술자, void *date, size_t byte_COUNT, int Setări,
                 struct sockaddr *adresa, socklen_t *adresa_lungime) {
    int cerere[2] = {(int)adresa, (int)adresa_lungime};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)date, byte_COUNT, Setări, (int)cerere));
}
int getsockname(int 파일서술자, struct sockaddr *adresa, socklen_t *adresa_lungime) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)adresa, (int)adresa_lungime, 0, 0));
}
int setsockopt(int 파일서술자, int strat_VALUE, int Setări_nume, const void *VALUE, socklen_t VALUE_lungime) {
    if (strat_VALUE != SOL_SOCKET || Setări_nume != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_lungime != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *oră_VALUE = VALUE;
    if (oră_VALUE->tv_sec < 0 || oră_VALUE->tv_sec > 2 || oră_VALUE->tv_usec < 0 || oră_VALUE->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = oră_VALUE->tv_sec * 1000 + (oră_VALUE->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VALUE) { return (VALUE << 8) | (VALUE >> 8); }
uint16_t ntohs(uint16_t VALUE) { return htons(VALUE); }
uint32_t htonl(uint32_t VALUE) {
    return (VALUE << 24) | ((VALUE << 8) & 0xff0000U) | ((VALUE >> 8) & 0xff00U) | (VALUE >> 24);
}
uint32_t ntohl(uint32_t VALUE) { return htonl(VALUE); }
int inet_pton(int 주소체계, const char *șir_VALUE, void *adresa) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!șir_VALUE || !adresa) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Pornește = șir_VALUE;
        while (*șir_VALUE >= '0' && *șir_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *șir_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Pornește == '0')) return 0;
        임시[칸] = VALUE;
        if (칸 < 3) { if (*șir_VALUE++ != '.') return 0; }
        else if (*șir_VALUE) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)adresa)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *adresa, char *șir_VALUE, socklen_t capacitate_VALUE) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!adresa || !șir_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = adresa;
    char 임시[16]; unsigned int lungime_VALUE = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int VALUE = 수[칸];
        if (VALUE >= 100) 임시[lungime_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[lungime_VALUE++] = '0' + VALUE / 10 % 10;
        임시[lungime_VALUE++] = '0' + VALUE % 10;
        if (칸 < 3) 임시[lungime_VALUE++] = '.';
    }
    임시[lungime_VALUE++] = 0;
    if (capacitate_VALUE < lungime_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < lungime_VALUE; 칸++) șir_VALUE[칸] = 임시[칸];
    return șir_VALUE;
}
