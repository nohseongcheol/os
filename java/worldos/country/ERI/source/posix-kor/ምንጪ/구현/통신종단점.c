#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ኣድራሻ, socklen_t ኣድራሻ_ንውሓት) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ኣድራሻ, ኣድራሻ_ንውሓት, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ሓበሬታ, size_t 바이트수, int ኣቀማምጣታት,
               const struct sockaddr *ኣድራሻ, socklen_t ኣድራሻ_ንውሓት) {
    int 요청[2] = {(int)ኣድራሻ, ኣድራሻ_ንውሓት};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ሓበሬታ, 바이트수, ኣቀማምጣታት, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ሓበሬታ, size_t 바이트수, int ኣቀማምጣታት,
                 struct sockaddr *ኣድራሻ, socklen_t *ኣድራሻ_ንውሓት) {
    int 요청[2] = {(int)ኣድራሻ, (int)ኣድራሻ_ንውሓት};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ሓበሬታ, 바이트수, ኣቀማምጣታት, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ኣድራሻ, socklen_t *ኣድራሻ_ንውሓት) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ኣድራሻ, (int)ኣድራሻ_ንውሓት, 0, 0));
}
int setsockopt(int 파일서술자, int ንጻፍ_ዋጋ, int ኣቀማምጣታት_ሽም, const void *ዋጋ, socklen_t ዋጋ_ንውሓት) {
    if (ንጻፍ_ዋጋ != SOL_SOCKET || ኣቀማምጣታት_ሽም != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ዋጋ) { errno = EFAULT; return -1; }
    if (ዋጋ_ንውሓት != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = ዋጋ;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ዋጋ) { return (ዋጋ << 8) | (ዋጋ >> 8); }
uint16_t ntohs(uint16_t ዋጋ) { return htons(ዋጋ); }
uint32_t htonl(uint32_t ዋጋ) {
    return (ዋጋ << 24) | ((ዋጋ << 8) & 0xff0000U) | ((ዋጋ >> 8) & 0xff00U) | (ዋጋ >> 24);
}
uint32_t ntohl(uint32_t ዋጋ) { return htonl(ዋጋ); }
int inet_pton(int 주소체계, const char *ሕብረ_ቁምፊ_ዋጋ, void *ኣድራሻ) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ሕብረ_ቁምፊ_ዋጋ || !ኣድራሻ) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int መሰኩዒ_ምእታው = 0; መሰኩዒ_ምእታው < 4; መሰኩዒ_ምእታው++) {
        int ዋጋ = 0, 자릿수 = 0;
        const char *ኣኺድ = ሕብረ_ቁምፊ_ዋጋ;
        while (*ሕብረ_ቁምፊ_ዋጋ >= '0' && *ሕብረ_ቁምፊ_ዋጋ <= '9') {
            if (++자릿수 > 3) return 0;
            ዋጋ = ዋጋ * 10 + *ሕብረ_ቁምፊ_ዋጋ++ - '0';
        }
        if (!자릿수 || ዋጋ > 255 || (자릿수 > 1 && *ኣኺድ == '0')) return 0;
        임시[መሰኩዒ_ምእታው] = ዋጋ;
        if (መሰኩዒ_ምእታው < 3) { if (*ሕብረ_ቁምፊ_ዋጋ++ != '.') return 0; }
        else if (*ሕብረ_ቁምፊ_ዋጋ) return 0;
    }
    for (int መሰኩዒ_ምእታው = 0; መሰኩዒ_ምእታው < 4; መሰኩዒ_ምእታው++) ((unsigned char *)ኣድራሻ)[መሰኩዒ_ምእታው] = 임시[መሰኩዒ_ምእታው];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ኣድራሻ, char *ሕብረ_ቁምፊ_ዋጋ, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ኣድራሻ || !ሕብረ_ቁምፊ_ዋጋ) { errno = EFAULT; return 0; }
    const unsigned char *수 = ኣድራሻ;
    char 임시[16]; unsigned int ንውሓት_ዋጋ = 0;
    for (int መሰኩዒ_ምእታው = 0; መሰኩዒ_ምእታው < 4; መሰኩዒ_ምእታው++) {
        unsigned int ዋጋ = 수[መሰኩዒ_ምእታው];
        if (ዋጋ >= 100) 임시[ንውሓት_ዋጋ++] = '0' + ዋጋ / 100;
        if (ዋጋ >= 10) 임시[ንውሓት_ዋጋ++] = '0' + ዋጋ / 10 % 10;
        임시[ንውሓት_ዋጋ++] = '0' + ዋጋ % 10;
        if (መሰኩዒ_ምእታው < 3) 임시[ንውሓት_ዋጋ++] = '.';
    }
    임시[ንውሓት_ዋጋ++] = 0;
    if (용량 < ንውሓት_ዋጋ) { errno = ENOSPC; return 0; }
    for (unsigned int መሰኩዒ_ምእታው = 0; መሰኩዒ_ምእታው < ንውሓት_ዋጋ; መሰኩዒ_ምእታው++) ሕብረ_ቁምፊ_ዋጋ[መሰኩዒ_ምእታው] = 임시[መሰኩዒ_ምእታው];
    return ሕብረ_ቁምፊ_ዋጋ;
}
