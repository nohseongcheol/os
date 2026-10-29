#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ناونیشان, socklen_t ناونیشان_درێژی) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ناونیشان, ناونیشان_درێژی, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *دەیتا, size_t 바이트수, int ڕێكبەندەكان,
               const struct sockaddr *ناونیشان, socklen_t ناونیشان_درێژی) {
    int 요청[2] = {(int)ناونیشان, ناونیشان_درێژی};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)دەیتا, 바이트수, ڕێكبەندەكان, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *دەیتا, size_t 바이트수, int ڕێكبەندەكان,
                 struct sockaddr *ناونیشان, socklen_t *ناونیشان_درێژی) {
    int 요청[2] = {(int)ناونیشان, (int)ناونیشان_درێژی};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)دەیتا, 바이트수, ڕێكبەندەكان, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ناونیشان, socklen_t *ناونیشان_درێژی) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ناونیشان, (int)ناونیشان_درێژی, 0, 0));
}
int setsockopt(int 파일서술자, int چین_نرخ, int ڕێكبەندەكان_ناو, const void *نرخ, socklen_t نرخ_درێژی) {
    if (چین_نرخ != SOL_SOCKET || ڕێكبەندەكان_ناو != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!نرخ) { errno = EFAULT; return -1; }
    if (نرخ_درێژی != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *کات_نرخ = نرخ;
    if (کات_نرخ->tv_sec < 0 || کات_نرخ->tv_sec > 2 || کات_نرخ->tv_usec < 0 || کات_نرخ->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = کات_نرخ->tv_sec * 1000 + (کات_نرخ->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t نرخ) { return (نرخ << 8) | (نرخ >> 8); }
uint16_t ntohs(uint16_t نرخ) { return htons(نرخ); }
uint32_t htonl(uint32_t نرخ) {
    return (نرخ << 24) | ((نرخ << 8) & 0xff0000U) | ((نرخ >> 8) & 0xff00U) | (نرخ >> 24);
}
uint32_t ntohl(uint32_t نرخ) { return htonl(نرخ); }
int inet_pton(int 주소체계, const char *رست_نرخ, void *ناونیشان) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!رست_نرخ || !ناونیشان) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین = 0; کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین < 4; کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین++) {
        int نرخ = 0, 자릿수 = 0;
        const char *ڕادان = رست_نرخ;
        while (*رست_نرخ >= '0' && *رست_نرخ <= '9') {
            if (++자릿수 > 3) return 0;
            نرخ = نرخ * 10 + *رست_نرخ++ - '0';
        }
        if (!자릿수 || نرخ > 255 || (자릿수 > 1 && *ڕادان == '0')) return 0;
        임시[کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین] = نرخ;
        if (کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین < 3) { if (*رست_نرخ++ != '.') return 0; }
        else if (*رست_نرخ) return 0;
    }
    for (int کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین = 0; کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین < 4; کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین++) ((unsigned char *)ناونیشان)[کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین] = 임시[کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ناونیشان, char *رست_نرخ, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ناونیشان || !رست_نرخ) { errno = EFAULT; return 0; }
    const unsigned char *수 = ناونیشان;
    char 임시[16]; unsigned int درێژی_نرخ = 0;
    for (int کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین = 0; کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین < 4; کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین++) {
        unsigned int نرخ = 수[کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین];
        if (نرخ >= 100) 임시[درێژی_نرخ++] = '0' + نرخ / 100;
        if (نرخ >= 10) 임시[درێژی_نرخ++] = '0' + نرخ / 10 % 10;
        임시[درێژی_نرخ++] = '0' + نرخ % 10;
        if (کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین < 3) 임시[درێژی_نرخ++] = '.';
    }
    임시[درێژی_نرخ++] = 0;
    if (용량 < درێژی_نرخ) { errno = ENOSPC; return 0; }
    for (unsigned int کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین = 0; کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین < درێژی_نرخ; کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین++) رست_نرخ[کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین] = 임시[کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین];
    return رست_نرخ;
}
