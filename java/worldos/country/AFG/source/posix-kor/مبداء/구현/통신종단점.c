#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *آدرس, socklen_t آدرس_طول) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)آدرس, آدرس_طول, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *داده_ها, size_t 바이트수, int تنظیمات,
               const struct sockaddr *آدرس, socklen_t آدرس_طول) {
    int 요청[2] = {(int)آدرس, آدرس_طول};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)داده_ها, 바이트수, تنظیمات, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *داده_ها, size_t 바이트수, int تنظیمات,
                 struct sockaddr *آدرس, socklen_t *آدرس_طول) {
    int 요청[2] = {(int)آدرس, (int)آدرس_طول};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)داده_ها, 바이트수, تنظیمات, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *آدرس, socklen_t *آدرس_طول) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)آدرس, (int)آدرس_طول, 0, 0));
}
int setsockopt(int 파일서술자, int لایه_مقدار, int تنظیمات_نام, const void *مقدار, socklen_t مقدار_طول) {
    if (لایه_مقدار != SOL_SOCKET || تنظیمات_نام != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!مقدار) { errno = EFAULT; return -1; }
    if (مقدار_طول != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *زمان_مقدار = مقدار;
    if (زمان_مقدار->tv_sec < 0 || زمان_مقدار->tv_sec > 2 || زمان_مقدار->tv_usec < 0 || زمان_مقدار->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = زمان_مقدار->tv_sec * 1000 + (زمان_مقدار->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t مقدار) { return (مقدار << 8) | (مقدار >> 8); }
uint16_t ntohs(uint16_t مقدار) { return htons(مقدار); }
uint32_t htonl(uint32_t مقدار) {
    return (مقدار << 24) | ((مقدار << 8) & 0xff0000U) | ((مقدار >> 8) & 0xff00U) | (مقدار >> 24);
}
uint32_t ntohl(uint32_t مقدار) { return htonl(مقدار); }
int inet_pton(int 주소체계, const char *رشته_مقدار_6ca8363c, void *آدرس) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!رشته_مقدار_6ca8363c || !آدرس) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int شکاف_ورودی = 0; شکاف_ورودی < 4; شکاف_ورودی++) {
        int مقدار = 0, 자릿수 = 0;
        const char *اجرا_2 = رشته_مقدار_6ca8363c;
        while (*رشته_مقدار_6ca8363c >= '0' && *رشته_مقدار_6ca8363c <= '9') {
            if (++자릿수 > 3) return 0;
            مقدار = مقدار * 10 + *رشته_مقدار_6ca8363c++ - '0';
        }
        if (!자릿수 || مقدار > 255 || (자릿수 > 1 && *اجرا_2 == '0')) return 0;
        임시[شکاف_ورودی] = مقدار;
        if (شکاف_ورودی < 3) { if (*رشته_مقدار_6ca8363c++ != '.') return 0; }
        else if (*رشته_مقدار_6ca8363c) return 0;
    }
    for (int شکاف_ورودی = 0; شکاف_ورودی < 4; شکاف_ورودی++) ((unsigned char *)آدرس)[شکاف_ورودی] = 임시[شکاف_ورودی];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *آدرس, char *رشته_مقدار_6ca8363c, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!آدرس || !رشته_مقدار_6ca8363c) { errno = EFAULT; return 0; }
    const unsigned char *수 = آدرس;
    char 임시[16]; unsigned int طول_مقدار = 0;
    for (int شکاف_ورودی = 0; شکاف_ورودی < 4; شکاف_ورودی++) {
        unsigned int مقدار = 수[شکاف_ورودی];
        if (مقدار >= 100) 임시[طول_مقدار++] = '0' + مقدار / 100;
        if (مقدار >= 10) 임시[طول_مقدار++] = '0' + مقدار / 10 % 10;
        임시[طول_مقدار++] = '0' + مقدار % 10;
        if (شکاف_ورودی < 3) 임시[طول_مقدار++] = '.';
    }
    임시[طول_مقدار++] = 0;
    if (용량 < طول_مقدار) { errno = ENOSPC; return 0; }
    for (unsigned int شکاف_ورودی = 0; شکاف_ورودی < طول_مقدار; شکاف_ورودی++) رشته_مقدار_6ca8363c[شکاف_ورودی] = 임시[شکاف_ورودی];
    return رشته_مقدار_6ca8363c;
}
