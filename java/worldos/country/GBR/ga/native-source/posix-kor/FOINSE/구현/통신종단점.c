#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ADDRESS, socklen_t ADDRESS_fad) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ADDRESS, ADDRESS_fad, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *sonraí, size_t beart_COUNT, int Socruithe,
               const struct sockaddr *ADDRESS, socklen_t ADDRESS_fad) {
    int iarratas_HTTP[2] = {(int)ADDRESS, ADDRESS_fad};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)sonraí, beart_COUNT, Socruithe, (int)iarratas_HTTP));
}
ssize_t recvfrom(int 파일서술자, void *sonraí, size_t beart_COUNT, int Socruithe,
                 struct sockaddr *ADDRESS, socklen_t *ADDRESS_fad) {
    int iarratas_HTTP[2] = {(int)ADDRESS, (int)ADDRESS_fad};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)sonraí, beart_COUNT, Socruithe, (int)iarratas_HTTP));
}
int getsockname(int 파일서술자, struct sockaddr *ADDRESS, socklen_t *ADDRESS_fad) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ADDRESS, (int)ADDRESS_fad, 0, 0));
}
int setsockopt(int 파일서술자, int sraith_VALUE, int Socruithe_ainm, const void *VALUE, socklen_t VALUE_fad) {
    if (sraith_VALUE != SOL_SOCKET || Socruithe_ainm != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_fad != sizeof(struct timeval)) { errno = EINVAL; return -1; }
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
int inet_pton(int 주소체계, const char *teaghrán_VALUE, void *ADDRESS) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!teaghrán_VALUE || !ADDRESS) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int spás_iontráil = 0; spás_iontráil < 4; spás_iontráil++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Rith_2 = teaghrán_VALUE;
        while (*teaghrán_VALUE >= '0' && *teaghrán_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *teaghrán_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Rith_2 == '0')) return 0;
        임시[spás_iontráil] = VALUE;
        if (spás_iontráil < 3) { if (*teaghrán_VALUE++ != '.') return 0; }
        else if (*teaghrán_VALUE) return 0;
    }
    for (int spás_iontráil = 0; spás_iontráil < 4; spás_iontráil++) ((unsigned char *)ADDRESS)[spás_iontráil] = 임시[spás_iontráil];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ADDRESS, char *teaghrán_VALUE, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ADDRESS || !teaghrán_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = ADDRESS;
    char 임시[16]; unsigned int fad_VALUE = 0;
    for (int spás_iontráil = 0; spás_iontráil < 4; spás_iontráil++) {
        unsigned int VALUE = 수[spás_iontráil];
        if (VALUE >= 100) 임시[fad_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[fad_VALUE++] = '0' + VALUE / 10 % 10;
        임시[fad_VALUE++] = '0' + VALUE % 10;
        if (spás_iontráil < 3) 임시[fad_VALUE++] = '.';
    }
    임시[fad_VALUE++] = 0;
    if (용량 < fad_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int spás_iontráil = 0; spás_iontráil < fad_VALUE; spás_iontráil++) teaghrán_VALUE[spás_iontráil] = 임시[spás_iontráil];
    return teaghrán_VALUE;
}
