#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ئادرېس, socklen_t ئادرېس_ئۇزۇنلۇق) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ئادرېس, ئادرېس_ئۇزۇنلۇق, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *مەلۇمات, size_t 바이트수, int تەڭشەكلەر,
               const struct sockaddr *ئادرېس, socklen_t ئادرېس_ئۇزۇنلۇق) {
    int 요청[2] = {(int)ئادرېس, ئادرېس_ئۇزۇنلۇق};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)مەلۇمات, 바이트수, تەڭشەكلەر, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *مەلۇمات, size_t 바이트수, int تەڭشەكلەر,
                 struct sockaddr *ئادرېس, socklen_t *ئادرېس_ئۇزۇنلۇق) {
    int 요청[2] = {(int)ئادرېس, (int)ئادرېس_ئۇزۇنلۇق};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)مەلۇمات, 바이트수, تەڭشەكلەر, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ئادرېس, socklen_t *ئادرېس_ئۇزۇنلۇق) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ئادرېس, (int)ئادرېس_ئۇزۇنلۇق, 0, 0));
}
int setsockopt(int 파일서술자, int قەۋەت_قىممىتى, int تەڭشەك_نامى, const void *قىممىتى, socklen_t قىممىتى_ئۇزۇنلۇق) {
    if (قەۋەت_قىممىتى != SOL_SOCKET || تەڭشەك_نامى != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!قىممىتى) { errno = EFAULT; return -1; }
    if (قىممىتى_ئۇزۇنلۇق != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = قىممىتى;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t قىممىتى) { return (قىممىتى << 8) | (قىممىتى >> 8); }
uint16_t ntohs(uint16_t قىممىتى) { return htons(قىممىتى); }
uint32_t htonl(uint32_t قىممىتى) {
    return (قىممىتى << 24) | ((قىممىتى << 8) & 0xff0000U) | ((قىممىتى >> 8) & 0xff00U) | (قىممىتى >> 24);
}
uint32_t ntohl(uint32_t قىممىتى) { return htonl(قىممىتى); }
int inet_pton(int 주소체계, const char *ھەرپ_تىزمىسى_قىممىتى, void *ئادرېس) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ھەرپ_تىزمىسى_قىممىتى || !ئادرېس) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int ئوقۇر_كىرگۈزۈش = 0; ئوقۇر_كىرگۈزۈش < 4; ئوقۇر_كىرگۈزۈش++) {
        int قىممىتى = 0, 자릿수 = 0;
        const char *ئىجرا_قىل_2 = ھەرپ_تىزمىسى_قىممىتى;
        while (*ھەرپ_تىزمىسى_قىممىتى >= '0' && *ھەرپ_تىزمىسى_قىممىتى <= '9') {
            if (++자릿수 > 3) return 0;
            قىممىتى = قىممىتى * 10 + *ھەرپ_تىزمىسى_قىممىتى++ - '0';
        }
        if (!자릿수 || قىممىتى > 255 || (자릿수 > 1 && *ئىجرا_قىل_2 == '0')) return 0;
        임시[ئوقۇر_كىرگۈزۈش] = قىممىتى;
        if (ئوقۇر_كىرگۈزۈش < 3) { if (*ھەرپ_تىزمىسى_قىممىتى++ != '.') return 0; }
        else if (*ھەرپ_تىزمىسى_قىممىتى) return 0;
    }
    for (int ئوقۇر_كىرگۈزۈش = 0; ئوقۇر_كىرگۈزۈش < 4; ئوقۇر_كىرگۈزۈش++) ((unsigned char *)ئادرېس)[ئوقۇر_كىرگۈزۈش] = 임시[ئوقۇر_كىرگۈزۈش];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ئادرېس, char *ھەرپ_تىزمىسى_قىممىتى, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ئادرېس || !ھەرپ_تىزمىسى_قىممىتى) { errno = EFAULT; return 0; }
    const unsigned char *수 = ئادرېس;
    char 임시[16]; unsigned int ئۇزۇنلۇق_قىممىتى = 0;
    for (int ئوقۇر_كىرگۈزۈش = 0; ئوقۇر_كىرگۈزۈش < 4; ئوقۇر_كىرگۈزۈش++) {
        unsigned int قىممىتى = 수[ئوقۇر_كىرگۈزۈش];
        if (قىممىتى >= 100) 임시[ئۇزۇنلۇق_قىممىتى++] = '0' + قىممىتى / 100;
        if (قىممىتى >= 10) 임시[ئۇزۇنلۇق_قىممىتى++] = '0' + قىممىتى / 10 % 10;
        임시[ئۇزۇنلۇق_قىممىتى++] = '0' + قىممىتى % 10;
        if (ئوقۇر_كىرگۈزۈش < 3) 임시[ئۇزۇنلۇق_قىممىتى++] = '.';
    }
    임시[ئۇزۇنلۇق_قىممىتى++] = 0;
    if (용량 < ئۇزۇنلۇق_قىممىتى) { errno = ENOSPC; return 0; }
    for (unsigned int ئوقۇر_كىرگۈزۈش = 0; ئوقۇر_كىرگۈزۈش < ئۇزۇنلۇق_قىممىتى; ئوقۇر_كىرگۈزۈش++) ھەرپ_تىزمىسى_قىممىتى[ئوقۇر_كىرگۈزۈش] = 임시[ئوقۇر_كىرگۈزۈش];
    return ھەرپ_تىزمىسى_قىممىتى;
}
