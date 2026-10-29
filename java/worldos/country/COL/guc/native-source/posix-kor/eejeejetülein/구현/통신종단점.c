#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ejepüsee, socklen_t ejepüsee_akaliaa) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ejepüsee, ejepüsee_akaliaa, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *atijaaya, size_t 바이트수, int 설정,
               const struct sockaddr *ejepüsee, socklen_t ejepüsee_akaliaa) {
    int 요청[2] = {(int)ejepüsee, ejepüsee_akaliaa};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)atijaaya, 바이트수, 설정, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *atijaaya, size_t 바이트수, int 설정,
                 struct sockaddr *ejepüsee, socklen_t *ejepüsee_akaliaa) {
    int 요청[2] = {(int)ejepüsee, (int)ejepüsee_akaliaa};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)atijaaya, 바이트수, 설정, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ejepüsee, socklen_t *ejepüsee_akaliaa) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ejepüsee, (int)ejepüsee_akaliaa, 0, 0));
}
int setsockopt(int 파일서술자, int ayaleriaa_ajutuu, int 설정이름, const void *ajutuu, socklen_t ajutuu_akaliaa) {
    if (ayaleriaa_ajutuu != SOL_SOCKET || 설정이름 != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ajutuu) { errno = EFAULT; return -1; }
    if (ajutuu_akaliaa != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = ajutuu;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ajutuu) { return (ajutuu << 8) | (ajutuu >> 8); }
uint16_t ntohs(uint16_t ajutuu) { return htons(ajutuu); }
uint32_t htonl(uint32_t ajutuu) {
    return (ajutuu << 24) | ((ajutuu << 8) & 0xff0000U) | ((ajutuu >> 8) & 0xff00U) | (ajutuu >> 24);
}
uint32_t ntohl(uint32_t ajutuu) { return htonl(ajutuu); }
int inet_pton(int 주소체계, const char *kaleena_ajutuu, void *ejepüsee) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!kaleena_ajutuu || !ejepüsee) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int ajutuu = 0, 자릿수 = 0;
        const char *시작 = kaleena_ajutuu;
        while (*kaleena_ajutuu >= '0' && *kaleena_ajutuu <= '9') {
            if (++자릿수 > 3) return 0;
            ajutuu = ajutuu * 10 + *kaleena_ajutuu++ - '0';
        }
        if (!자릿수 || ajutuu > 255 || (자릿수 > 1 && *시작 == '0')) return 0;
        임시[칸] = ajutuu;
        if (칸 < 3) { if (*kaleena_ajutuu++ != '.') return 0; }
        else if (*kaleena_ajutuu) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)ejepüsee)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ejepüsee, char *kaleena_ajutuu, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ejepüsee || !kaleena_ajutuu) { errno = EFAULT; return 0; }
    const unsigned char *수 = ejepüsee;
    char 임시[16]; unsigned int akaliaa_ajutuu = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int ajutuu = 수[칸];
        if (ajutuu >= 100) 임시[akaliaa_ajutuu++] = '0' + ajutuu / 100;
        if (ajutuu >= 10) 임시[akaliaa_ajutuu++] = '0' + ajutuu / 10 % 10;
        임시[akaliaa_ajutuu++] = '0' + ajutuu % 10;
        if (칸 < 3) 임시[akaliaa_ajutuu++] = '.';
    }
    임시[akaliaa_ajutuu++] = 0;
    if (용량 < akaliaa_ajutuu) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < akaliaa_ajutuu; 칸++) kaleena_ajutuu[칸] = 임시[칸];
    return kaleena_ajutuu;
}
