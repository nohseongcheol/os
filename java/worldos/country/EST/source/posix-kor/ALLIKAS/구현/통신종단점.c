#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int kaasus_number) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, kaasus_number, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ADDRESS, socklen_t 주소길이) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ADDRESS, 주소길이, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *andmed, size_t bait_COUNT, int Seaded,
               const struct sockaddr *ADDRESS, socklen_t 주소길이) {
    int päring[2] = {(int)ADDRESS, 주소길이};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)andmed, bait_COUNT, Seaded, (int)päring));
}
ssize_t recvfrom(int 파일서술자, void *andmed, size_t bait_COUNT, int Seaded,
                 struct sockaddr *ADDRESS, socklen_t *주소길이) {
    int päring[2] = {(int)ADDRESS, (int)주소길이};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)andmed, bait_COUNT, Seaded, (int)päring));
}
int getsockname(int 파일서술자, struct sockaddr *ADDRESS, socklen_t *주소길이) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ADDRESS, (int)주소길이, 0, 0));
}
int setsockopt(int 파일서술자, int kiht_VALUE, int Sätted_nimetus, const void *VALUE, socklen_t 값길이) {
    if (kiht_VALUE != SOL_SOCKET || Sätted_nimetus != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (값길이 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *Aeg_VALUE = VALUE;
    if (Aeg_VALUE->tv_sec < 0 || Aeg_VALUE->tv_sec > 2 || Aeg_VALUE->tv_usec < 0 || Aeg_VALUE->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = Aeg_VALUE->tv_sec * 1000 + (Aeg_VALUE->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VALUE) { return (VALUE << 8) | (VALUE >> 8); }
uint16_t ntohs(uint16_t VALUE) { return htons(VALUE); }
uint32_t htonl(uint32_t VALUE) {
    return (VALUE << 24) | ((VALUE << 8) & 0xff0000U) | ((VALUE >> 8) & 0xff00U) | (VALUE >> 24);
}
uint32_t ntohl(uint32_t VALUE) { return htonl(VALUE); }
int inet_pton(int 주소체계, const char *string_VALUE, void *ADDRESS) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!string_VALUE || !ADDRESS) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Käivita_2 = string_VALUE;
        while (*string_VALUE >= '0' && *string_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *string_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Käivita_2 == '0')) return 0;
        임시[칸] = VALUE;
        if (칸 < 3) { if (*string_VALUE++ != '.') return 0; }
        else if (*string_VALUE) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)ADDRESS)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ADDRESS, char *string_VALUE, socklen_t võimsus_VALUE) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ADDRESS || !string_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *number = ADDRESS;
    char 임시[16]; unsigned int 길이 = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int VALUE = number[칸];
        if (VALUE >= 100) 임시[길이++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[길이++] = '0' + VALUE / 10 % 10;
        임시[길이++] = '0' + VALUE % 10;
        if (칸 < 3) 임시[길이++] = '.';
    }
    임시[길이++] = 0;
    if (võimsus_VALUE < 길이) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < 길이; 칸++) string_VALUE[칸] = 임시[칸];
    return string_VALUE;
}
