#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ಇಮೇಲ್, socklen_t ಇಮೇಲ್_ಉದ್ದ) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ಇಮೇಲ್, ಇಮೇಲ್_ಉದ್ದ, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ಡೇಟಾ, size_t 바이트수, int ಸಿದ್ಧತೆಗಳು,
               const struct sockaddr *ಇಮೇಲ್, socklen_t ಇಮೇಲ್_ಉದ್ದ) {
    int 요청[2] = {(int)ಇಮೇಲ್, ಇಮೇಲ್_ಉದ್ದ};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ಡೇಟಾ, 바이트수, ಸಿದ್ಧತೆಗಳು, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ಡೇಟಾ, size_t 바이트수, int ಸಿದ್ಧತೆಗಳು,
                 struct sockaddr *ಇಮೇಲ್, socklen_t *ಇಮೇಲ್_ಉದ್ದ) {
    int 요청[2] = {(int)ಇಮೇಲ್, (int)ಇಮೇಲ್_ಉದ್ದ};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ಡೇಟಾ, 바이트수, ಸಿದ್ಧತೆಗಳು, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ಇಮೇಲ್, socklen_t *ಇಮೇಲ್_ಉದ್ದ) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ಇಮೇಲ್, (int)ಇಮೇಲ್_ಉದ್ದ, 0, 0));
}
int setsockopt(int 파일서술자, int ಪದರ_ಮೌಲ್ಯ, int ಸೆಟ್ಟಿಂಗ್ಸ್_ಹೆಸರು, const void *ಮೌಲ್ಯ, socklen_t ಮೌಲ್ಯ_ಉದ್ದ) {
    if (ಪದರ_ಮೌಲ್ಯ != SOL_SOCKET || ಸೆಟ್ಟಿಂಗ್ಸ್_ಹೆಸರು != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ಮೌಲ್ಯ) { errno = EFAULT; return -1; }
    if (ಮೌಲ್ಯ_ಉದ್ದ != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *ಸಮಯ_ಮೌಲ್ಯ = ಮೌಲ್ಯ;
    if (ಸಮಯ_ಮೌಲ್ಯ->tv_sec < 0 || ಸಮಯ_ಮೌಲ್ಯ->tv_sec > 2 || ಸಮಯ_ಮೌಲ್ಯ->tv_usec < 0 || ಸಮಯ_ಮೌಲ್ಯ->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = ಸಮಯ_ಮೌಲ್ಯ->tv_sec * 1000 + (ಸಮಯ_ಮೌಲ್ಯ->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ಮೌಲ್ಯ) { return (ಮೌಲ್ಯ << 8) | (ಮೌಲ್ಯ >> 8); }
uint16_t ntohs(uint16_t ಮೌಲ್ಯ) { return htons(ಮೌಲ್ಯ); }
uint32_t htonl(uint32_t ಮೌಲ್ಯ) {
    return (ಮೌಲ್ಯ << 24) | ((ಮೌಲ್ಯ << 8) & 0xff0000U) | ((ಮೌಲ್ಯ >> 8) & 0xff00U) | (ಮೌಲ್ಯ >> 24);
}
uint32_t ntohl(uint32_t ಮೌಲ್ಯ) { return htonl(ಮೌಲ್ಯ); }
int inet_pton(int 주소체계, const char *ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ, void *ಇಮೇಲ್) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ || !ಇಮೇಲ್) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int ಸ್ಲಾಟ್_ನಮೂದು = 0; ಸ್ಲಾಟ್_ನಮೂದು < 4; ಸ್ಲಾಟ್_ನಮೂದು++) {
        int ಮೌಲ್ಯ = 0, 자릿수 = 0;
        const char *ಚಲಾಯಿಸು_2 = ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ;
        while (*ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ >= '0' && *ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ <= '9') {
            if (++자릿수 > 3) return 0;
            ಮೌಲ್ಯ = ಮೌಲ್ಯ * 10 + *ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ++ - '0';
        }
        if (!자릿수 || ಮೌಲ್ಯ > 255 || (자릿수 > 1 && *ಚಲಾಯಿಸು_2 == '0')) return 0;
        임시[ಸ್ಲಾಟ್_ನಮೂದು] = ಮೌಲ್ಯ;
        if (ಸ್ಲಾಟ್_ನಮೂದು < 3) { if (*ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ++ != '.') return 0; }
        else if (*ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ) return 0;
    }
    for (int ಸ್ಲಾಟ್_ನಮೂದು = 0; ಸ್ಲಾಟ್_ನಮೂದು < 4; ಸ್ಲಾಟ್_ನಮೂದು++) ((unsigned char *)ಇಮೇಲ್)[ಸ್ಲಾಟ್_ನಮೂದು] = 임시[ಸ್ಲಾಟ್_ನಮೂದು];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ಇಮೇಲ್, char *ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ಇಮೇಲ್ || !ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ) { errno = EFAULT; return 0; }
    const unsigned char *수 = ಇಮೇಲ್;
    char 임시[16]; unsigned int ಉದ್ದ_ಮೌಲ್ಯ = 0;
    for (int ಸ್ಲಾಟ್_ನಮೂದು = 0; ಸ್ಲಾಟ್_ನಮೂದು < 4; ಸ್ಲಾಟ್_ನಮೂದು++) {
        unsigned int ಮೌಲ್ಯ = 수[ಸ್ಲಾಟ್_ನಮೂದು];
        if (ಮೌಲ್ಯ >= 100) 임시[ಉದ್ದ_ಮೌಲ್ಯ++] = '0' + ಮೌಲ್ಯ / 100;
        if (ಮೌಲ್ಯ >= 10) 임시[ಉದ್ದ_ಮೌಲ್ಯ++] = '0' + ಮೌಲ್ಯ / 10 % 10;
        임시[ಉದ್ದ_ಮೌಲ್ಯ++] = '0' + ಮೌಲ್ಯ % 10;
        if (ಸ್ಲಾಟ್_ನಮೂದು < 3) 임시[ಉದ್ದ_ಮೌಲ್ಯ++] = '.';
    }
    임시[ಉದ್ದ_ಮೌಲ್ಯ++] = 0;
    if (용량 < ಉದ್ದ_ಮೌಲ್ಯ) { errno = ENOSPC; return 0; }
    for (unsigned int ಸ್ಲಾಟ್_ನಮೂದು = 0; ಸ್ಲಾಟ್_ನಮೂದು < ಉದ್ದ_ಮೌಲ್ಯ; ಸ್ಲಾಟ್_ನಮೂದು++) ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ[ಸ್ಲಾಟ್_ನಮೂದು] = 임시[ಸ್ಲಾಟ್_ನಮೂದು];
    return ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ;
}
