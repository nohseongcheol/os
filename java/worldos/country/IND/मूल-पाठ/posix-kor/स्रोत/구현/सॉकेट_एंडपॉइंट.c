#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *पता, socklen_t 주소길이) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)पता, 주소길이, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *आँकड़े, size_t 바이트수, int विन्यास,
               const struct sockaddr *पता, socklen_t 주소길이) {
    int अनुरोध[2] = {(int)पता, 주소길이};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)आँकड़े, 바이트수, विन्यास, (int)अनुरोध));
}
ssize_t recvfrom(int 파일서술자, void *आँकड़े, size_t 바이트수, int विन्यास,
                 struct sockaddr *पता, socklen_t *주소길이) {
    int अनुरोध[2] = {(int)पता, (int)주소길이};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)आँकड़े, 바이트수, विन्यास, (int)अनुरोध));
}
int getsockname(int 파일서술자, struct sockaddr *पता, socklen_t *주소길이) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)पता, (int)주소길이, 0, 0));
}
int setsockopt(int 파일서술자, int लेयर_मान, int सेटिंग_नाम, const void *मान, socklen_t 값길이) {
    if (लेयर_मान != SOL_SOCKET || सेटिंग_नाम != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!मान) { errno = EFAULT; return -1; }
    if (값길이 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *समय_उपयोगिता = मान;
    if (समय_उपयोगिता->tv_sec < 0 || समय_उपयोगिता->tv_sec > 2 || समय_उपयोगिता->tv_usec < 0 || समय_उपयोगिता->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = समय_उपयोगिता->tv_sec * 1000 + (समय_उपयोगिता->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t मान) { return (मान << 8) | (मान >> 8); }
uint16_t ntohs(uint16_t मान) { return htons(मान); }
uint32_t htonl(uint32_t मान) {
    return (मान << 24) | ((मान << 8) & 0xff0000U) | ((मान >> 8) & 0xff00U) | (मान >> 24);
}
uint32_t ntohl(uint32_t मान) { return htonl(मान); }
int inet_pton(int 주소체계, const char *स्ट्रिंग_मान, void *पता) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!स्ट्रिंग_मान || !पता) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int मान = 0, 자릿수 = 0;
        const char *चलाएँ = स्ट्रिंग_मान;
        while (*स्ट्रिंग_मान >= '0' && *स्ट्रिंग_मान <= '9') {
            if (++자릿수 > 3) return 0;
            मान = मान * 10 + *स्ट्रिंग_मान++ - '0';
        }
        if (!자릿수 || मान > 255 || (자릿수 > 1 && *चलाएँ == '0')) return 0;
        임시[칸] = मान;
        if (칸 < 3) { if (*स्ट्रिंग_मान++ != '.') return 0; }
        else if (*स्ट्रिंग_मान) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)पता)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *पता, char *स्ट्रिंग_मान, socklen_t क्षमता_मान) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!पता || !स्ट्रिंग_मान) { errno = EFAULT; return 0; }
    const unsigned char *수 = पता;
    char 임시[16]; unsigned int 길이 = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int मान = 수[칸];
        if (मान >= 100) 임시[길이++] = '0' + मान / 100;
        if (मान >= 10) 임시[길이++] = '0' + मान / 10 % 10;
        임시[길이++] = '0' + मान % 10;
        if (칸 < 3) 임시[길이++] = '.';
    }
    임시[길이++] = 0;
    if (क्षमता_मान < 길이) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < 길이; 칸++) स्ट्रिंग_मान[칸] = 임시[칸];
    return स्ट्रिंग_मान;
}
