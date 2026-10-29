#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ਪਤਾ, socklen_t ਪਤਾ_ਲੰਬਾਈ) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ਪਤਾ, ਪਤਾ_ਲੰਬਾਈ, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ਸਮੱਗਰੀ, size_t 바이트수, int ਸੈਟਿੰਗ,
               const struct sockaddr *ਪਤਾ, socklen_t ਪਤਾ_ਲੰਬਾਈ) {
    int 요청[2] = {(int)ਪਤਾ, ਪਤਾ_ਲੰਬਾਈ};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ਸਮੱਗਰੀ, 바이트수, ਸੈਟਿੰਗ, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ਸਮੱਗਰੀ, size_t 바이트수, int ਸੈਟਿੰਗ,
                 struct sockaddr *ਪਤਾ, socklen_t *ਪਤਾ_ਲੰਬਾਈ) {
    int 요청[2] = {(int)ਪਤਾ, (int)ਪਤਾ_ਲੰਬਾਈ};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ਸਮੱਗਰੀ, 바이트수, ਸੈਟਿੰਗ, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ਪਤਾ, socklen_t *ਪਤਾ_ਲੰਬਾਈ) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ਪਤਾ, (int)ਪਤਾ_ਲੰਬਾਈ, 0, 0));
}
int setsockopt(int 파일서술자, int ਲੇਅਰ_ਕੀਮਤ, int ਸੈਟਿੰਗਾਂ_ਨਾਮ, const void *ਕੀਮਤ, socklen_t ਕੀਮਤ_ਲੰਬਾਈ) {
    if (ਲੇਅਰ_ਕੀਮਤ != SOL_SOCKET || ਸੈਟਿੰਗਾਂ_ਨਾਮ != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ਕੀਮਤ) { errno = EFAULT; return -1; }
    if (ਕੀਮਤ_ਲੰਬਾਈ != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = ਕੀਮਤ;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ਕੀਮਤ) { return (ਕੀਮਤ << 8) | (ਕੀਮਤ >> 8); }
uint16_t ntohs(uint16_t ਕੀਮਤ) { return htons(ਕੀਮਤ); }
uint32_t htonl(uint32_t ਕੀਮਤ) {
    return (ਕੀਮਤ << 24) | ((ਕੀਮਤ << 8) & 0xff0000U) | ((ਕੀਮਤ >> 8) & 0xff00U) | (ਕੀਮਤ >> 24);
}
uint32_t ntohl(uint32_t ਕੀਮਤ) { return htonl(ਕੀਮਤ); }
int inet_pton(int 주소체계, const char *ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ, void *ਪਤਾ) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ || !ਪਤਾ) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int ਸਲੌਟ_ਦਾਖਲਾ = 0; ਸਲੌਟ_ਦਾਖਲਾ < 4; ਸਲੌਟ_ਦਾਖਲਾ++) {
        int ਕੀਮਤ = 0, 자릿수 = 0;
        const char *ਚਲਾਓ_2 = ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ;
        while (*ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ >= '0' && *ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ <= '9') {
            if (++자릿수 > 3) return 0;
            ਕੀਮਤ = ਕੀਮਤ * 10 + *ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ++ - '0';
        }
        if (!자릿수 || ਕੀਮਤ > 255 || (자릿수 > 1 && *ਚਲਾਓ_2 == '0')) return 0;
        임시[ਸਲੌਟ_ਦਾਖਲਾ] = ਕੀਮਤ;
        if (ਸਲੌਟ_ਦਾਖਲਾ < 3) { if (*ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ++ != '.') return 0; }
        else if (*ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ) return 0;
    }
    for (int ਸਲੌਟ_ਦਾਖਲਾ = 0; ਸਲੌਟ_ਦਾਖਲਾ < 4; ਸਲੌਟ_ਦਾਖਲਾ++) ((unsigned char *)ਪਤਾ)[ਸਲੌਟ_ਦਾਖਲਾ] = 임시[ਸਲੌਟ_ਦਾਖਲਾ];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ਪਤਾ, char *ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ਪਤਾ || !ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ) { errno = EFAULT; return 0; }
    const unsigned char *수 = ਪਤਾ;
    char 임시[16]; unsigned int ਲੰਬਾਈ_ਕੀਮਤ = 0;
    for (int ਸਲੌਟ_ਦਾਖਲਾ = 0; ਸਲੌਟ_ਦਾਖਲਾ < 4; ਸਲੌਟ_ਦਾਖਲਾ++) {
        unsigned int ਕੀਮਤ = 수[ਸਲੌਟ_ਦਾਖਲਾ];
        if (ਕੀਮਤ >= 100) 임시[ਲੰਬਾਈ_ਕੀਮਤ++] = '0' + ਕੀਮਤ / 100;
        if (ਕੀਮਤ >= 10) 임시[ਲੰਬਾਈ_ਕੀਮਤ++] = '0' + ਕੀਮਤ / 10 % 10;
        임시[ਲੰਬਾਈ_ਕੀਮਤ++] = '0' + ਕੀਮਤ % 10;
        if (ਸਲੌਟ_ਦਾਖਲਾ < 3) 임시[ਲੰਬਾਈ_ਕੀਮਤ++] = '.';
    }
    임시[ਲੰਬਾਈ_ਕੀਮਤ++] = 0;
    if (용량 < ਲੰਬਾਈ_ਕੀਮਤ) { errno = ENOSPC; return 0; }
    for (unsigned int ਸਲੌਟ_ਦਾਖਲਾ = 0; ਸਲੌਟ_ਦਾਖਲਾ < ਲੰਬਾਈ_ਕੀਮਤ; ਸਲੌਟ_ਦਾਖਲਾ++) ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ[ਸਲੌਟ_ਦਾਖਲਾ] = 임시[ਸਲੌਟ_ਦਾਖਲਾ];
    return ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ;
}
