#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int līgums_numurs) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, līgums_numurs, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *adrese, socklen_t 주소길이) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)adrese, 주소길이, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *dati, size_t byte_COUNT, int Uzstādījumi,
               const struct sockaddr *adrese, socklen_t 주소길이) {
    int pieprasījums[2] = {(int)adrese, 주소길이};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)dati, byte_COUNT, Uzstādījumi, (int)pieprasījums));
}
ssize_t recvfrom(int 파일서술자, void *dati, size_t byte_COUNT, int Uzstādījumi,
                 struct sockaddr *adrese, socklen_t *주소길이) {
    int pieprasījums[2] = {(int)adrese, (int)주소길이};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)dati, byte_COUNT, Uzstādījumi, (int)pieprasījums));
}
int getsockname(int 파일서술자, struct sockaddr *adrese, socklen_t *주소길이) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)adrese, (int)주소길이, 0, 0));
}
int setsockopt(int 파일서술자, int slānis_VALUE, int Iestatījumi_nosaukums, const void *VALUE, socklen_t 값길이) {
    if (slānis_VALUE != SOL_SOCKET || Iestatījumi_nosaukums != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (값길이 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
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
int inet_pton(int 주소체계, const char *virkne_VALUE, void *adrese) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!virkne_VALUE || !adrese) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Palaist = virkne_VALUE;
        while (*virkne_VALUE >= '0' && *virkne_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *virkne_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Palaist == '0')) return 0;
        임시[칸] = VALUE;
        if (칸 < 3) { if (*virkne_VALUE++ != '.') return 0; }
        else if (*virkne_VALUE) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)adrese)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *adrese, char *virkne_VALUE, socklen_t noslodze_VALUE) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!adrese || !virkne_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *numurs = adrese;
    char 임시[16]; unsigned int 길이 = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int VALUE = numurs[칸];
        if (VALUE >= 100) 임시[길이++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[길이++] = '0' + VALUE / 10 % 10;
        임시[길이++] = '0' + VALUE % 10;
        if (칸 < 3) 임시[길이++] = '.';
    }
    임시[길이++] = 0;
    if (noslodze_VALUE < 길이) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < 길이; 칸++) virkne_VALUE[칸] = 임시[칸];
    return virkne_VALUE;
}
