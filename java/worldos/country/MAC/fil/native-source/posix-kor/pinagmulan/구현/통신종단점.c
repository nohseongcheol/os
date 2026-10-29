#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *email, socklen_t email_haba) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)email, email_haba, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t byte_COUNT, int Mga_Setting,
               const struct sockaddr *email, socklen_t email_haba) {
    int 요청[2] = {(int)email, email_haba};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, byte_COUNT, Mga_Setting, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t byte_COUNT, int Mga_Setting,
                 struct sockaddr *email, socklen_t *email_haba) {
    int 요청[2] = {(int)email, (int)email_haba};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, byte_COUNT, Mga_Setting, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *email, socklen_t *email_haba) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)email, (int)email_haba, 0, 0));
}
int setsockopt(int 파일서술자, int patong_VALUE, int Mga_Setting_pangalan, const void *VALUE, socklen_t VALUE_haba) {
    if (patong_VALUE != SOL_SOCKET || Mga_Setting_pangalan != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_haba != sizeof(struct timeval)) { errno = EINVAL; return -1; }
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
int inet_pton(int 주소체계, const char *string_VALUE, void *email) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!string_VALUE || !email) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int espasyo_pagpasok = 0; espasyo_pagpasok < 4; espasyo_pagpasok++) {
        int VALUE = 0, 자릿수 = 0;
        const char *run = string_VALUE;
        while (*string_VALUE >= '0' && *string_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *string_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *run == '0')) return 0;
        임시[espasyo_pagpasok] = VALUE;
        if (espasyo_pagpasok < 3) { if (*string_VALUE++ != '.') return 0; }
        else if (*string_VALUE) return 0;
    }
    for (int espasyo_pagpasok = 0; espasyo_pagpasok < 4; espasyo_pagpasok++) ((unsigned char *)email)[espasyo_pagpasok] = 임시[espasyo_pagpasok];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *email, char *string_VALUE, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!email || !string_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = email;
    char 임시[16]; unsigned int haba_VALUE = 0;
    for (int espasyo_pagpasok = 0; espasyo_pagpasok < 4; espasyo_pagpasok++) {
        unsigned int VALUE = 수[espasyo_pagpasok];
        if (VALUE >= 100) 임시[haba_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[haba_VALUE++] = '0' + VALUE / 10 % 10;
        임시[haba_VALUE++] = '0' + VALUE % 10;
        if (espasyo_pagpasok < 3) 임시[haba_VALUE++] = '.';
    }
    임시[haba_VALUE++] = 0;
    if (용량 < haba_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int espasyo_pagpasok = 0; espasyo_pagpasok < haba_VALUE; espasyo_pagpasok++) string_VALUE[espasyo_pagpasok] = 임시[espasyo_pagpasok];
    return string_VALUE;
}
