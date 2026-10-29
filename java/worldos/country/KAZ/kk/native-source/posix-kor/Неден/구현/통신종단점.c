#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *мекенжай, socklen_t мекенжай_ұзындық) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)мекенжай, мекенжай_ұзындық, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *деректер, size_t 바이트수, int Баптаулар,
               const struct sockaddr *мекенжай, socklen_t мекенжай_ұзындық) {
    int 요청[2] = {(int)мекенжай, мекенжай_ұзындық};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)деректер, 바이트수, Баптаулар, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *деректер, size_t 바이트수, int Баптаулар,
                 struct sockaddr *мекенжай, socklen_t *мекенжай_ұзындық) {
    int 요청[2] = {(int)мекенжай, (int)мекенжай_ұзындық};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)деректер, 바이트수, Баптаулар, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *мекенжай, socklen_t *мекенжай_ұзындық) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)мекенжай, (int)мекенжай_ұзындық, 0, 0));
}
int setsockopt(int 파일서술자, int қабат_мән, int Параметрлер_аты, const void *мән, socklen_t мән_ұзындық) {
    if (қабат_мән != SOL_SOCKET || Параметрлер_аты != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!мән) { errno = EFAULT; return -1; }
    if (мән_ұзындық != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *уақыт_мән = мән;
    if (уақыт_мән->tv_sec < 0 || уақыт_мән->tv_sec > 2 || уақыт_мән->tv_usec < 0 || уақыт_мән->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = уақыт_мән->tv_sec * 1000 + (уақыт_мән->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t мән) { return (мән << 8) | (мән >> 8); }
uint16_t ntohs(uint16_t мән) { return htons(мән); }
uint32_t htonl(uint32_t мән) {
    return (мән << 24) | ((мән << 8) & 0xff0000U) | ((мән >> 8) & 0xff00U) | (мән >> 24);
}
uint32_t ntohl(uint32_t мән) { return htonl(мән); }
int inet_pton(int 주소체계, const char *жол_мән_6ca8363c, void *мекенжай) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!жол_мән_6ca8363c || !мекенжай) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int мән = 0, 자릿수 = 0;
        const char *Орындау_2 = жол_мән_6ca8363c;
        while (*жол_мән_6ca8363c >= '0' && *жол_мән_6ca8363c <= '9') {
            if (++자릿수 > 3) return 0;
            мән = мән * 10 + *жол_мән_6ca8363c++ - '0';
        }
        if (!자릿수 || мән > 255 || (자릿수 > 1 && *Орындау_2 == '0')) return 0;
        임시[칸] = мән;
        if (칸 < 3) { if (*жол_мән_6ca8363c++ != '.') return 0; }
        else if (*жол_мән_6ca8363c) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)мекенжай)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *мекенжай, char *жол_мән_6ca8363c, socklen_t мүмкіндік_мән) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!мекенжай || !жол_мән_6ca8363c) { errno = EFAULT; return 0; }
    const unsigned char *수 = мекенжай;
    char 임시[16]; unsigned int ұзындық_мән = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int мән = 수[칸];
        if (мән >= 100) 임시[ұзындық_мән++] = '0' + мән / 100;
        if (мән >= 10) 임시[ұзындық_мән++] = '0' + мән / 10 % 10;
        임시[ұзындық_мән++] = '0' + мән % 10;
        if (칸 < 3) 임시[ұзындық_мән++] = '.';
    }
    임시[ұзындық_мән++] = 0;
    if (мүмкіндік_мән < ұзындық_мән) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < ұзындық_мән; 칸++) жол_мән_6ca8363c[칸] = 임시[칸];
    return жол_мән_6ca8363c;
}
