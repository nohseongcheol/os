#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *አድራሻ, socklen_t አድራሻ_ርዝመት) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)አድራሻ, አድራሻ_ርዝመት, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ውሂብ, size_t 바이트수, int ማሰናጃዎች,
               const struct sockaddr *አድራሻ, socklen_t አድራሻ_ርዝመት) {
    int 요청[2] = {(int)አድራሻ, አድራሻ_ርዝመት};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ውሂብ, 바이트수, ማሰናጃዎች, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ውሂብ, size_t 바이트수, int ማሰናጃዎች,
                 struct sockaddr *አድራሻ, socklen_t *አድራሻ_ርዝመት) {
    int 요청[2] = {(int)አድራሻ, (int)አድራሻ_ርዝመት};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ውሂብ, 바이트수, ማሰናጃዎች, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *አድራሻ, socklen_t *አድራሻ_ርዝመት) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)አድራሻ, (int)አድራሻ_ርዝመት, 0, 0));
}
int setsockopt(int 파일서술자, int ንብርብር_እሴት, int ቅንብሮች_ስም, const void *እሴት, socklen_t እሴት_ርዝመት) {
    if (ንብርብር_እሴት != SOL_SOCKET || ቅንብሮች_ስም != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!እሴት) { errno = EFAULT; return -1; }
    if (እሴት_ርዝመት != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *ጊዜ_እሴት = እሴት;
    if (ጊዜ_እሴት->tv_sec < 0 || ጊዜ_እሴት->tv_sec > 2 || ጊዜ_እሴት->tv_usec < 0 || ጊዜ_እሴት->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = ጊዜ_እሴት->tv_sec * 1000 + (ጊዜ_እሴት->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t እሴት) { return (እሴት << 8) | (እሴት >> 8); }
uint16_t ntohs(uint16_t እሴት) { return htons(እሴት); }
uint32_t htonl(uint32_t እሴት) {
    return (እሴት << 24) | ((እሴት << 8) & 0xff0000U) | ((እሴት >> 8) & 0xff00U) | (እሴት >> 24);
}
uint32_t ntohl(uint32_t እሴት) { return htonl(እሴት); }
int inet_pton(int 주소체계, const char *ኅብረቁምፊ_እሴት, void *አድራሻ) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ኅብረቁምፊ_እሴት || !አድራሻ) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int ማስገቢያ_ቀዳዳ_ምዝግብ = 0; ማስገቢያ_ቀዳዳ_ምዝግብ < 4; ማስገቢያ_ቀዳዳ_ምዝግብ++) {
        int እሴት = 0, 자릿수 = 0;
        const char *ማስኬጃ = ኅብረቁምፊ_እሴት;
        while (*ኅብረቁምፊ_እሴት >= '0' && *ኅብረቁምፊ_እሴት <= '9') {
            if (++자릿수 > 3) return 0;
            እሴት = እሴት * 10 + *ኅብረቁምፊ_እሴት++ - '0';
        }
        if (!자릿수 || እሴት > 255 || (자릿수 > 1 && *ማስኬጃ == '0')) return 0;
        임시[ማስገቢያ_ቀዳዳ_ምዝግብ] = እሴት;
        if (ማስገቢያ_ቀዳዳ_ምዝግብ < 3) { if (*ኅብረቁምፊ_እሴት++ != '.') return 0; }
        else if (*ኅብረቁምፊ_እሴት) return 0;
    }
    for (int ማስገቢያ_ቀዳዳ_ምዝግብ = 0; ማስገቢያ_ቀዳዳ_ምዝግብ < 4; ማስገቢያ_ቀዳዳ_ምዝግብ++) ((unsigned char *)አድራሻ)[ማስገቢያ_ቀዳዳ_ምዝግብ] = 임시[ማስገቢያ_ቀዳዳ_ምዝግብ];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *አድራሻ, char *ኅብረቁምፊ_እሴት, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!አድራሻ || !ኅብረቁምፊ_እሴት) { errno = EFAULT; return 0; }
    const unsigned char *수 = አድራሻ;
    char 임시[16]; unsigned int ርዝመት_እሴት = 0;
    for (int ማስገቢያ_ቀዳዳ_ምዝግብ = 0; ማስገቢያ_ቀዳዳ_ምዝግብ < 4; ማስገቢያ_ቀዳዳ_ምዝግብ++) {
        unsigned int እሴት = 수[ማስገቢያ_ቀዳዳ_ምዝግብ];
        if (እሴት >= 100) 임시[ርዝመት_እሴት++] = '0' + እሴት / 100;
        if (እሴት >= 10) 임시[ርዝመት_እሴት++] = '0' + እሴት / 10 % 10;
        임시[ርዝመት_እሴት++] = '0' + እሴት % 10;
        if (ማስገቢያ_ቀዳዳ_ምዝግብ < 3) 임시[ርዝመት_እሴት++] = '.';
    }
    임시[ርዝመት_እሴት++] = 0;
    if (용량 < ርዝመት_እሴት) { errno = ENOSPC; return 0; }
    for (unsigned int ማስገቢያ_ቀዳዳ_ምዝግብ = 0; ማስገቢያ_ቀዳዳ_ምዝግብ < ርዝመት_እሴት; ማስገቢያ_ቀዳዳ_ምዝግብ++) ኅብረቁምፊ_እሴት[ማስገቢያ_ቀዳዳ_ምዝግብ] = 임시[ማስገቢያ_ቀዳዳ_ምዝግብ];
    return ኅብረቁምፊ_እሴት;
}
