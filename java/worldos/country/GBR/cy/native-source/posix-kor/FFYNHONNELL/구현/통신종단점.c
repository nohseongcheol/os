#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ADDRESS, socklen_t ADDRESS_hyd) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ADDRESS, ADDRESS_hyd, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t beit_COUNT, int Gosodiadau,
               const struct sockaddr *ADDRESS, socklen_t ADDRESS_hyd) {
    int cais_HTTP[2] = {(int)ADDRESS, ADDRESS_hyd};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, beit_COUNT, Gosodiadau, (int)cais_HTTP));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t beit_COUNT, int Gosodiadau,
                 struct sockaddr *ADDRESS, socklen_t *ADDRESS_hyd) {
    int cais_HTTP[2] = {(int)ADDRESS, (int)ADDRESS_hyd};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, beit_COUNT, Gosodiadau, (int)cais_HTTP));
}
int getsockname(int 파일서술자, struct sockaddr *ADDRESS, socklen_t *ADDRESS_hyd) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ADDRESS, (int)ADDRESS_hyd, 0, 0));
}
int setsockopt(int 파일서술자, int haen_VALUE, int Gosodiadau_enw, const void *VALUE, socklen_t VALUE_hyd) {
    if (haen_VALUE != SOL_SOCKET || Gosodiadau_enw != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_hyd != sizeof(struct timeval)) { errno = EINVAL; return -1; }
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
int inet_pton(int 주소체계, const char *testun_VALUE, void *ADDRESS) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!testun_VALUE || !ADDRESS) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int slot_cofnod = 0; slot_cofnod < 4; slot_cofnod++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Gweithredu_2 = testun_VALUE;
        while (*testun_VALUE >= '0' && *testun_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *testun_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Gweithredu_2 == '0')) return 0;
        임시[slot_cofnod] = VALUE;
        if (slot_cofnod < 3) { if (*testun_VALUE++ != '.') return 0; }
        else if (*testun_VALUE) return 0;
    }
    for (int slot_cofnod = 0; slot_cofnod < 4; slot_cofnod++) ((unsigned char *)ADDRESS)[slot_cofnod] = 임시[slot_cofnod];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ADDRESS, char *testun_VALUE, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ADDRESS || !testun_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = ADDRESS;
    char 임시[16]; unsigned int hyd_VALUE = 0;
    for (int slot_cofnod = 0; slot_cofnod < 4; slot_cofnod++) {
        unsigned int VALUE = 수[slot_cofnod];
        if (VALUE >= 100) 임시[hyd_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[hyd_VALUE++] = '0' + VALUE / 10 % 10;
        임시[hyd_VALUE++] = '0' + VALUE % 10;
        if (slot_cofnod < 3) 임시[hyd_VALUE++] = '.';
    }
    임시[hyd_VALUE++] = 0;
    if (용량 < hyd_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int slot_cofnod = 0; slot_cofnod < hyd_VALUE; slot_cofnod++) testun_VALUE[slot_cofnod] = 임시[slot_cofnod];
    return testun_VALUE;
}
