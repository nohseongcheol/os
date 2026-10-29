#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *پتو, socklen_t پتو_لمبائي) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)پتو, پتو_لمبائي, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ڪوائف, size_t 바이트수, int سيٽنگون,
               const struct sockaddr *پتو, socklen_t پتو_لمبائي) {
    int 요청[2] = {(int)پتو, پتو_لمبائي};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ڪوائف, 바이트수, سيٽنگون, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ڪوائف, size_t 바이트수, int سيٽنگون,
                 struct sockaddr *پتو, socklen_t *پتو_لمبائي) {
    int 요청[2] = {(int)پتو, (int)پتو_لمبائي};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ڪوائف, 바이트수, سيٽنگون, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *پتو, socklen_t *پتو_لمبائي) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)پتو, (int)پتو_لمبائي, 0, 0));
}
int setsockopt(int 파일서술자, int پرت_قدر, int سيٽنگون_نالو, const void *قدر, socklen_t قدر_لمبائي) {
    if (پرت_قدر != SOL_SOCKET || سيٽنگون_نالو != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!قدر) { errno = EFAULT; return -1; }
    if (قدر_لمبائي != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = قدر;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t قدر) { return (قدر << 8) | (قدر >> 8); }
uint16_t ntohs(uint16_t قدر) { return htons(قدر); }
uint32_t htonl(uint32_t قدر) {
    return (قدر << 24) | ((قدر << 8) & 0xff0000U) | ((قدر >> 8) & 0xff00U) | (قدر >> 24);
}
uint32_t ntohl(uint32_t قدر) { return htonl(قدر); }
int inet_pton(int 주소체계, const char *اسٽرنگ_قدر, void *پتو) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!اسٽرنگ_قدر || !پتو) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int سوراخ_داخلا = 0; سوراخ_داخلا < 4; سوراخ_داخلا++) {
        int قدر = 0, 자릿수 = 0;
        const char *هلائڻ = اسٽرنگ_قدر;
        while (*اسٽرنگ_قدر >= '0' && *اسٽرنگ_قدر <= '9') {
            if (++자릿수 > 3) return 0;
            قدر = قدر * 10 + *اسٽرنگ_قدر++ - '0';
        }
        if (!자릿수 || قدر > 255 || (자릿수 > 1 && *هلائڻ == '0')) return 0;
        임시[سوراخ_داخلا] = قدر;
        if (سوراخ_داخلا < 3) { if (*اسٽرنگ_قدر++ != '.') return 0; }
        else if (*اسٽرنگ_قدر) return 0;
    }
    for (int سوراخ_داخلا = 0; سوراخ_داخلا < 4; سوراخ_داخلا++) ((unsigned char *)پتو)[سوراخ_داخلا] = 임시[سوراخ_داخلا];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *پتو, char *اسٽرنگ_قدر, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!پتو || !اسٽرنگ_قدر) { errno = EFAULT; return 0; }
    const unsigned char *수 = پتو;
    char 임시[16]; unsigned int لمبائي_قدر = 0;
    for (int سوراخ_داخلا = 0; سوراخ_داخلا < 4; سوراخ_داخلا++) {
        unsigned int قدر = 수[سوراخ_داخلا];
        if (قدر >= 100) 임시[لمبائي_قدر++] = '0' + قدر / 100;
        if (قدر >= 10) 임시[لمبائي_قدر++] = '0' + قدر / 10 % 10;
        임시[لمبائي_قدر++] = '0' + قدر % 10;
        if (سوراخ_داخلا < 3) 임시[لمبائي_قدر++] = '.';
    }
    임시[لمبائي_قدر++] = 0;
    if (용량 < لمبائي_قدر) { errno = ENOSPC; return 0; }
    for (unsigned int سوراخ_داخلا = 0; سوراخ_داخلا < لمبائي_قدر; سوراخ_داخلا++) اسٽرنگ_قدر[سوراخ_داخلا] = 임시[سوراخ_داخلا];
    return اسٽرنگ_قدر;
}
