#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ଠିକଣା, socklen_t ଠିକଣା_ଦୈର୍ଘ୍ୟ) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ଠିକଣା, ଠିକଣା_ଦୈର୍ଘ୍ୟ, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ଡାଟା, size_t 바이트수, int ବିନ୍ଯାସ,
               const struct sockaddr *ଠିକଣା, socklen_t ଠିକଣା_ଦୈର୍ଘ୍ୟ) {
    int 요청[2] = {(int)ଠିକଣା, ଠିକଣା_ଦୈର୍ଘ୍ୟ};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ଡାଟା, 바이트수, ବିନ୍ଯାସ, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ଡାଟା, size_t 바이트수, int ବିନ୍ଯାସ,
                 struct sockaddr *ଠିକଣା, socklen_t *ଠିକଣା_ଦୈର୍ଘ୍ୟ) {
    int 요청[2] = {(int)ଠିକଣା, (int)ଠିକଣା_ଦୈର୍ଘ୍ୟ};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ଡାଟା, 바이트수, ବିନ୍ଯାସ, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ଠିକଣା, socklen_t *ଠିକଣା_ଦୈର୍ଘ୍ୟ) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ଠିକଣା, (int)ଠିକଣା_ଦୈର୍ଘ୍ୟ, 0, 0));
}
int setsockopt(int 파일서술자, int ସ୍ତର_ମୂଲ୍ୟ, int ସେଟିଂସ୍_ନାମ, const void *ମୂଲ୍ୟ, socklen_t ମୂଲ୍ୟ_ଦୈର୍ଘ୍ୟ) {
    if (ସ୍ତର_ମୂଲ୍ୟ != SOL_SOCKET || ସେଟିଂସ୍_ନାମ != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ମୂଲ୍ୟ) { errno = EFAULT; return -1; }
    if (ମୂଲ୍ୟ_ଦୈର୍ଘ୍ୟ != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *ସମୟ_ମୂଲ୍ୟ = ମୂଲ୍ୟ;
    if (ସମୟ_ମୂଲ୍ୟ->tv_sec < 0 || ସମୟ_ମୂଲ୍ୟ->tv_sec > 2 || ସମୟ_ମୂଲ୍ୟ->tv_usec < 0 || ସମୟ_ମୂଲ୍ୟ->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = ସମୟ_ମୂଲ୍ୟ->tv_sec * 1000 + (ସମୟ_ମୂଲ୍ୟ->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ମୂଲ୍ୟ) { return (ମୂଲ୍ୟ << 8) | (ମୂଲ୍ୟ >> 8); }
uint16_t ntohs(uint16_t ମୂଲ୍ୟ) { return htons(ମୂଲ୍ୟ); }
uint32_t htonl(uint32_t ମୂଲ୍ୟ) {
    return (ମୂଲ୍ୟ << 24) | ((ମୂଲ୍ୟ << 8) & 0xff0000U) | ((ମୂଲ୍ୟ >> 8) & 0xff00U) | (ମୂଲ୍ୟ >> 24);
}
uint32_t ntohl(uint32_t ମୂଲ୍ୟ) { return htonl(ମୂଲ୍ୟ); }
int inet_pton(int 주소체계, const char *ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ, void *ଠିକଣା) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ || !ଠିକଣା) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି = 0; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି < 4; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି++) {
        int ମୂଲ୍ୟ = 0, 자릿수 = 0;
        const char *ଚଳାନ୍ତୁ = ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ;
        while (*ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ >= '0' && *ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ <= '9') {
            if (++자릿수 > 3) return 0;
            ମୂଲ୍ୟ = ମୂଲ୍ୟ * 10 + *ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ++ - '0';
        }
        if (!자릿수 || ମୂଲ୍ୟ > 255 || (자릿수 > 1 && *ଚଳାନ୍ତୁ == '0')) return 0;
        임시[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି] = ମୂଲ୍ୟ;
        if (ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି < 3) { if (*ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ++ != '.') return 0; }
        else if (*ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ) return 0;
    }
    for (int ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି = 0; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି < 4; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି++) ((unsigned char *)ଠିକଣା)[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି] = 임시[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ଠିକଣା, char *ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ଠିକଣା || !ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ) { errno = EFAULT; return 0; }
    const unsigned char *수 = ଠିକଣା;
    char 임시[16]; unsigned int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = 0;
    for (int ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି = 0; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି < 4; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି++) {
        unsigned int ମୂଲ୍ୟ = 수[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି];
        if (ମୂଲ୍ୟ >= 100) 임시[ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ++] = '0' + ମୂଲ୍ୟ / 100;
        if (ମୂଲ୍ୟ >= 10) 임시[ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ++] = '0' + ମୂଲ୍ୟ / 10 % 10;
        임시[ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ++] = '0' + ମୂଲ୍ୟ % 10;
        if (ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି < 3) 임시[ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ++] = '.';
    }
    임시[ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ++] = 0;
    if (용량 < ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) { errno = ENOSPC; return 0; }
    for (unsigned int ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି = 0; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି < ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି++) ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି] = 임시[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି];
    return ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ;
}
