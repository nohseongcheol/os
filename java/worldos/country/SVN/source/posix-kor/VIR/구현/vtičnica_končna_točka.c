#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *naslov, socklen_t 주소길이) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)naslov, 주소길이, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *podatki, size_t bajt_COUNT, int Nastavitve,
               const struct sockaddr *naslov, socklen_t 주소길이) {
    int zahteva[2] = {(int)naslov, 주소길이};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)podatki, bajt_COUNT, Nastavitve, (int)zahteva));
}
ssize_t recvfrom(int 파일서술자, void *podatki, size_t bajt_COUNT, int Nastavitve,
                 struct sockaddr *naslov, socklen_t *주소길이) {
    int zahteva[2] = {(int)naslov, (int)주소길이};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)podatki, bajt_COUNT, Nastavitve, (int)zahteva));
}
int getsockname(int 파일서술자, struct sockaddr *naslov, socklen_t *주소길이) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)naslov, (int)주소길이, 0, 0));
}
int setsockopt(int 파일서술자, int sloj_VALUE, int Nastavitve_ime, const void *VALUE, socklen_t 값길이) {
    if (sloj_VALUE != SOL_SOCKET || Nastavitve_ime != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (값길이 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
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
int inet_pton(int 주소체계, const char *niz_VALUE, void *naslov) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!niz_VALUE || !naslov) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Zaženi = niz_VALUE;
        while (*niz_VALUE >= '0' && *niz_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *niz_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Zaženi == '0')) return 0;
        임시[칸] = VALUE;
        if (칸 < 3) { if (*niz_VALUE++ != '.') return 0; }
        else if (*niz_VALUE) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)naslov)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *naslov, char *niz_VALUE, socklen_t zmogljivost_VALUE) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!naslov || !niz_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = naslov;
    char 임시[16]; unsigned int 길이 = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int VALUE = 수[칸];
        if (VALUE >= 100) 임시[길이++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[길이++] = '0' + VALUE / 10 % 10;
        임시[길이++] = '0' + VALUE % 10;
        if (칸 < 3) 임시[길이++] = '.';
    }
    임시[길이++] = 0;
    if (zmogljivost_VALUE < 길이) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < 길이; 칸++) niz_VALUE[칸] = 임시[칸];
    return niz_VALUE;
}
