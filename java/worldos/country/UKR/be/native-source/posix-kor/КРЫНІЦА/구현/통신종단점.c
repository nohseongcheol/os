#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *адрас, socklen_t адрас_даўжыня) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)адрас, адрас_даўжыня, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *дадзеныя, size_t 바이트수, int Усталёўкі,
               const struct sockaddr *адрас, socklen_t адрас_даўжыня) {
    int 요청[2] = {(int)адрас, адрас_даўжыня};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)дадзеныя, 바이트수, Усталёўкі, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *дадзеныя, size_t 바이트수, int Усталёўкі,
                 struct sockaddr *адрас, socklen_t *адрас_даўжыня) {
    int 요청[2] = {(int)адрас, (int)адрас_даўжыня};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)дадзеныя, 바이트수, Усталёўкі, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *адрас, socklen_t *адрас_даўжыня) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)адрас, (int)адрас_даўжыня, 0, 0));
}
int setsockopt(int 파일서술자, int слой_значэнне, int Налады_імя, const void *значэнне, socklen_t значэнне_даўжыня) {
    if (слой_значэнне != SOL_SOCKET || Налады_імя != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!значэнне) { errno = EFAULT; return -1; }
    if (значэнне_даўжыня != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *час_значэнне = значэнне;
    if (час_значэнне->tv_sec < 0 || час_значэнне->tv_sec > 2 || час_значэнне->tv_usec < 0 || час_значэнне->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = час_значэнне->tv_sec * 1000 + (час_значэнне->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t значэнне) { return (значэнне << 8) | (значэнне >> 8); }
uint16_t ntohs(uint16_t значэнне) { return htons(значэнне); }
uint32_t htonl(uint32_t значэнне) {
    return (значэнне << 24) | ((значэнне << 8) & 0xff0000U) | ((значэнне >> 8) & 0xff00U) | (значэнне >> 24);
}
uint32_t ntohl(uint32_t значэнне) { return htonl(значэнне); }
int inet_pton(int 주소체계, const char *радок_значэнне, void *адрас) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!радок_значэнне || !адрас) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int слот_увядзенне = 0; слот_увядзенне < 4; слот_увядзенне++) {
        int значэнне = 0, 자릿수 = 0;
        const char *Выканаць = радок_значэнне;
        while (*радок_значэнне >= '0' && *радок_значэнне <= '9') {
            if (++자릿수 > 3) return 0;
            значэнне = значэнне * 10 + *радок_значэнне++ - '0';
        }
        if (!자릿수 || значэнне > 255 || (자릿수 > 1 && *Выканаць == '0')) return 0;
        임시[слот_увядзенне] = значэнне;
        if (слот_увядзенне < 3) { if (*радок_значэнне++ != '.') return 0; }
        else if (*радок_значэнне) return 0;
    }
    for (int слот_увядзенне = 0; слот_увядзенне < 4; слот_увядзенне++) ((unsigned char *)адрас)[слот_увядзенне] = 임시[слот_увядзенне];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *адрас, char *радок_значэнне, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!адрас || !радок_значэнне) { errno = EFAULT; return 0; }
    const unsigned char *수 = адрас;
    char 임시[16]; unsigned int даўжыня_значэнне = 0;
    for (int слот_увядзенне = 0; слот_увядзенне < 4; слот_увядзенне++) {
        unsigned int значэнне = 수[слот_увядзенне];
        if (значэнне >= 100) 임시[даўжыня_значэнне++] = '0' + значэнне / 100;
        if (значэнне >= 10) 임시[даўжыня_значэнне++] = '0' + значэнне / 10 % 10;
        임시[даўжыня_значэнне++] = '0' + значэнне % 10;
        if (слот_увядзенне < 3) 임시[даўжыня_значэнне++] = '.';
    }
    임시[даўжыня_значэнне++] = 0;
    if (용량 < даўжыня_значэнне) { errno = ENOSPC; return 0; }
    for (unsigned int слот_увядзенне = 0; слот_увядзенне < даўжыня_значэнне; слот_увядзенне++) радок_значэнне[слот_увядзенне] = 임시[слот_увядзенне];
    return радок_значэнне;
}
