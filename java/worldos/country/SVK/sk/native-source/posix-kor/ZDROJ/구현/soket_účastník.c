#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *adresa, socklen_t adresa_dĺžka) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)adresa, adresa_dĺžka, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *údaje, size_t Byte_COUNT, int Nastavenia,
               const struct sockaddr *adresa, socklen_t adresa_dĺžka) {
    int požiadavka[2] = {(int)adresa, adresa_dĺžka};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)údaje, Byte_COUNT, Nastavenia, (int)požiadavka));
}
ssize_t recvfrom(int 파일서술자, void *údaje, size_t Byte_COUNT, int Nastavenia,
                 struct sockaddr *adresa, socklen_t *adresa_dĺžka) {
    int požiadavka[2] = {(int)adresa, (int)adresa_dĺžka};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)údaje, Byte_COUNT, Nastavenia, (int)požiadavka));
}
int getsockname(int 파일서술자, struct sockaddr *adresa, socklen_t *adresa_dĺžka) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)adresa, (int)adresa_dĺžka, 0, 0));
}
int setsockopt(int 파일서술자, int vrstva_VALUE, int Nastavenia_názov, const void *VALUE, socklen_t VALUE_dĺžka) {
    if (vrstva_VALUE != SOL_SOCKET || Nastavenia_názov != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_dĺžka != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *čas_VALUE = VALUE;
    if (čas_VALUE->tv_sec < 0 || čas_VALUE->tv_sec > 2 || čas_VALUE->tv_usec < 0 || čas_VALUE->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = čas_VALUE->tv_sec * 1000 + (čas_VALUE->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VALUE) { return (VALUE << 8) | (VALUE >> 8); }
uint16_t ntohs(uint16_t VALUE) { return htons(VALUE); }
uint32_t htonl(uint32_t VALUE) {
    return (VALUE << 24) | ((VALUE << 8) & 0xff0000U) | ((VALUE >> 8) & 0xff00U) | (VALUE >> 24);
}
uint32_t ntohl(uint32_t VALUE) { return htonl(VALUE); }
int inet_pton(int 주소체계, const char *reťazec_VALUE, void *adresa) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!reťazec_VALUE || !adresa) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Spustiť_2 = reťazec_VALUE;
        while (*reťazec_VALUE >= '0' && *reťazec_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *reťazec_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Spustiť_2 == '0')) return 0;
        임시[칸] = VALUE;
        if (칸 < 3) { if (*reťazec_VALUE++ != '.') return 0; }
        else if (*reťazec_VALUE) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)adresa)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *adresa, char *reťazec_VALUE, socklen_t kapacita_VALUE) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!adresa || !reťazec_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = adresa;
    char 임시[16]; unsigned int dĺžka_VALUE = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int VALUE = 수[칸];
        if (VALUE >= 100) 임시[dĺžka_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[dĺžka_VALUE++] = '0' + VALUE / 10 % 10;
        임시[dĺžka_VALUE++] = '0' + VALUE % 10;
        if (칸 < 3) 임시[dĺžka_VALUE++] = '.';
    }
    임시[dĺžka_VALUE++] = 0;
    if (kapacita_VALUE < dĺžka_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < dĺžka_VALUE; 칸++) reťazec_VALUE[칸] = 임시[칸];
    return reťazec_VALUE;
}
