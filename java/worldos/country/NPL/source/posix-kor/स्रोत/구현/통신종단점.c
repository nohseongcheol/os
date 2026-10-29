#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ठेगाना, socklen_t ठेगाना_लम्बाइ) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ठेगाना, ठेगाना_लम्बाइ, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *लगत, size_t 바이트수, int सेटिङ,
               const struct sockaddr *ठेगाना, socklen_t ठेगाना_लम्बाइ) {
    int 요청[2] = {(int)ठेगाना, ठेगाना_लम्बाइ};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)लगत, 바이트수, सेटिङ, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *लगत, size_t 바이트수, int सेटिङ,
                 struct sockaddr *ठेगाना, socklen_t *ठेगाना_लम्बाइ) {
    int 요청[2] = {(int)ठेगाना, (int)ठेगाना_लम्बाइ};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)लगत, 바이트수, सेटिङ, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ठेगाना, socklen_t *ठेगाना_लम्बाइ) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ठेगाना, (int)ठेगाना_लम्बाइ, 0, 0));
}
int setsockopt(int 파일서술자, int तह_मान, int सेटिङहरू_नाम, const void *मान, socklen_t मान_लम्बाइ) {
    if (तह_मान != SOL_SOCKET || सेटिङहरू_नाम != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!मान) { errno = EFAULT; return -1; }
    if (मान_लम्बाइ != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = मान;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t मान) { return (मान << 8) | (मान >> 8); }
uint16_t ntohs(uint16_t मान) { return htons(मान); }
uint32_t htonl(uint32_t मान) {
    return (मान << 24) | ((मान << 8) & 0xff0000U) | ((मान >> 8) & 0xff00U) | (मान >> 24);
}
uint32_t ntohl(uint32_t मान) { return htonl(मान); }
int inet_pton(int 주소체계, const char *स्ट्रिङ_मान, void *ठेगाना) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!स्ट्रिङ_मान || !ठेगाना) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int स्लट_प्रविष्टि = 0; स्लट_प्रविष्टि < 4; स्लट_प्रविष्टि++) {
        int मान = 0, 자릿수 = 0;
        const char *चलाउनुहोस् = स्ट्रिङ_मान;
        while (*स्ट्रिङ_मान >= '0' && *स्ट्रिङ_मान <= '9') {
            if (++자릿수 > 3) return 0;
            मान = मान * 10 + *स्ट्रिङ_मान++ - '0';
        }
        if (!자릿수 || मान > 255 || (자릿수 > 1 && *चलाउनुहोस् == '0')) return 0;
        임시[स्लट_प्रविष्टि] = मान;
        if (स्लट_प्रविष्टि < 3) { if (*स्ट्रिङ_मान++ != '.') return 0; }
        else if (*स्ट्रिङ_मान) return 0;
    }
    for (int स्लट_प्रविष्टि = 0; स्लट_प्रविष्टि < 4; स्लट_प्रविष्टि++) ((unsigned char *)ठेगाना)[स्लट_प्रविष्टि] = 임시[स्लट_प्रविष्टि];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ठेगाना, char *स्ट्रिङ_मान, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ठेगाना || !स्ट्रिङ_मान) { errno = EFAULT; return 0; }
    const unsigned char *수 = ठेगाना;
    char 임시[16]; unsigned int लम्बाइ_मान = 0;
    for (int स्लट_प्रविष्टि = 0; स्लट_प्रविष्टि < 4; स्लट_प्रविष्टि++) {
        unsigned int मान = 수[स्लट_प्रविष्टि];
        if (मान >= 100) 임시[लम्बाइ_मान++] = '0' + मान / 100;
        if (मान >= 10) 임시[लम्बाइ_मान++] = '0' + मान / 10 % 10;
        임시[लम्बाइ_मान++] = '0' + मान % 10;
        if (स्लट_प्रविष्टि < 3) 임시[लम्बाइ_मान++] = '.';
    }
    임시[लम्बाइ_मान++] = 0;
    if (용량 < लम्बाइ_मान) { errno = ENOSPC; return 0; }
    for (unsigned int स्लट_प्रविष्टि = 0; स्लट_प्रविष्टि < लम्बाइ_मान; स्लट_प्रविष्टि++) स्ट्रिङ_मान[स्लट_प्रविष्टि] = 임시[स्लट_प्रविष्टि];
    return स्ट्रिङ_मान;
}
