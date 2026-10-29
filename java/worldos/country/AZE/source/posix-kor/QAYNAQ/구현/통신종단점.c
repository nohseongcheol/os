#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ünvan, socklen_t ünvan_uzunluq) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ünvan, ünvan_uzunluq, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *verilənlər, size_t bayt_COUNT, int Sazlama,
               const struct sockaddr *ünvan, socklen_t ünvan_uzunluq) {
    int HTTP_sorğusu[2] = {(int)ünvan, ünvan_uzunluq};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)verilənlər, bayt_COUNT, Sazlama, (int)HTTP_sorğusu));
}
ssize_t recvfrom(int 파일서술자, void *verilənlər, size_t bayt_COUNT, int Sazlama,
                 struct sockaddr *ünvan, socklen_t *ünvan_uzunluq) {
    int HTTP_sorğusu[2] = {(int)ünvan, (int)ünvan_uzunluq};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)verilənlər, bayt_COUNT, Sazlama, (int)HTTP_sorğusu));
}
int getsockname(int 파일서술자, struct sockaddr *ünvan, socklen_t *ünvan_uzunluq) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ünvan, (int)ünvan_uzunluq, 0, 0));
}
int setsockopt(int 파일서술자, int lay_VALUE, int Parametrlər_ad, const void *VALUE, socklen_t VALUE_uzunluq) {
    if (lay_VALUE != SOL_SOCKET || Parametrlər_ad != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_uzunluq != sizeof(struct timeval)) { errno = EINVAL; return -1; }
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
int inet_pton(int 주소체계, const char *sətir_VALUE, void *ünvan) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!sətir_VALUE || !ünvan) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int slot_daxiletmə = 0; slot_daxiletmə < 4; slot_daxiletmə++) {
        int VALUE = 0, 자릿수 = 0;
        const char *İcra_Et = sətir_VALUE;
        while (*sətir_VALUE >= '0' && *sətir_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *sətir_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *İcra_Et == '0')) return 0;
        임시[slot_daxiletmə] = VALUE;
        if (slot_daxiletmə < 3) { if (*sətir_VALUE++ != '.') return 0; }
        else if (*sətir_VALUE) return 0;
    }
    for (int slot_daxiletmə = 0; slot_daxiletmə < 4; slot_daxiletmə++) ((unsigned char *)ünvan)[slot_daxiletmə] = 임시[slot_daxiletmə];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ünvan, char *sətir_VALUE, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ünvan || !sətir_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = ünvan;
    char 임시[16]; unsigned int uzunluq_VALUE = 0;
    for (int slot_daxiletmə = 0; slot_daxiletmə < 4; slot_daxiletmə++) {
        unsigned int VALUE = 수[slot_daxiletmə];
        if (VALUE >= 100) 임시[uzunluq_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[uzunluq_VALUE++] = '0' + VALUE / 10 % 10;
        임시[uzunluq_VALUE++] = '0' + VALUE % 10;
        if (slot_daxiletmə < 3) 임시[uzunluq_VALUE++] = '.';
    }
    임시[uzunluq_VALUE++] = 0;
    if (용량 < uzunluq_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int slot_daxiletmə = 0; slot_daxiletmə < uzunluq_VALUE; slot_daxiletmə++) sətir_VALUE[slot_daxiletmə] = 임시[slot_daxiletmə];
    return sətir_VALUE;
}
