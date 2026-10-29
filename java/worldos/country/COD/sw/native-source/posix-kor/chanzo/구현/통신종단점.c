#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *anwani, socklen_t anwani_urefu) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)anwani, anwani_urefu, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t 바이트수, int Mipangilio,
               const struct sockaddr *anwani, socklen_t anwani_urefu) {
    int 요청[2] = {(int)anwani, anwani_urefu};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, 바이트수, Mipangilio, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t 바이트수, int Mipangilio,
                 struct sockaddr *anwani, socklen_t *anwani_urefu) {
    int 요청[2] = {(int)anwani, (int)anwani_urefu};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, 바이트수, Mipangilio, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *anwani, socklen_t *anwani_urefu) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)anwani, (int)anwani_urefu, 0, 0));
}
int setsockopt(int 파일서술자, int tabaka_thamani, int Mipangilio_jina, const void *thamani, socklen_t thamani_urefu) {
    if (tabaka_thamani != SOL_SOCKET || Mipangilio_jina != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!thamani) { errno = EFAULT; return -1; }
    if (thamani_urefu != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *saa_thamani_4692cef5 = thamani;
    if (saa_thamani_4692cef5->tv_sec < 0 || saa_thamani_4692cef5->tv_sec > 2 || saa_thamani_4692cef5->tv_usec < 0 || saa_thamani_4692cef5->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = saa_thamani_4692cef5->tv_sec * 1000 + (saa_thamani_4692cef5->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t thamani) { return (thamani << 8) | (thamani >> 8); }
uint16_t ntohs(uint16_t thamani) { return htons(thamani); }
uint32_t htonl(uint32_t thamani) {
    return (thamani << 24) | ((thamani << 8) & 0xff0000U) | ((thamani >> 8) & 0xff00U) | (thamani >> 24);
}
uint32_t ntohl(uint32_t thamani) { return htonl(thamani); }
int inet_pton(int 주소체계, const char *tungo_thamani, void *anwani) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!tungo_thamani || !anwani) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int Sloti_ingizo = 0; Sloti_ingizo < 4; Sloti_ingizo++) {
        int thamani = 0, 자릿수 = 0;
        const char *endesha = tungo_thamani;
        while (*tungo_thamani >= '0' && *tungo_thamani <= '9') {
            if (++자릿수 > 3) return 0;
            thamani = thamani * 10 + *tungo_thamani++ - '0';
        }
        if (!자릿수 || thamani > 255 || (자릿수 > 1 && *endesha == '0')) return 0;
        임시[Sloti_ingizo] = thamani;
        if (Sloti_ingizo < 3) { if (*tungo_thamani++ != '.') return 0; }
        else if (*tungo_thamani) return 0;
    }
    for (int Sloti_ingizo = 0; Sloti_ingizo < 4; Sloti_ingizo++) ((unsigned char *)anwani)[Sloti_ingizo] = 임시[Sloti_ingizo];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *anwani, char *tungo_thamani, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!anwani || !tungo_thamani) { errno = EFAULT; return 0; }
    const unsigned char *수 = anwani;
    char 임시[16]; unsigned int urefu_thamani = 0;
    for (int Sloti_ingizo = 0; Sloti_ingizo < 4; Sloti_ingizo++) {
        unsigned int thamani = 수[Sloti_ingizo];
        if (thamani >= 100) 임시[urefu_thamani++] = '0' + thamani / 100;
        if (thamani >= 10) 임시[urefu_thamani++] = '0' + thamani / 10 % 10;
        임시[urefu_thamani++] = '0' + thamani % 10;
        if (Sloti_ingizo < 3) 임시[urefu_thamani++] = '.';
    }
    임시[urefu_thamani++] = 0;
    if (용량 < urefu_thamani) { errno = ENOSPC; return 0; }
    for (unsigned int Sloti_ingizo = 0; Sloti_ingizo < urefu_thamani; Sloti_ingizo++) tungo_thamani[Sloti_ingizo] = 임시[Sloti_ingizo];
    return tungo_thamani;
}
