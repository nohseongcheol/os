#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *հասցե, socklen_t հասցե_տեւողություն) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)հասցե, հասցե_տեւողություն, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *տվյալ, size_t 바이트수, int Նախընտրանքներ,
               const struct sockaddr *հասցե, socklen_t հասցե_տեւողություն) {
    int 요청[2] = {(int)հասցե, հասցե_տեւողություն};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)տվյալ, 바이트수, Նախընտրանքներ, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *տվյալ, size_t 바이트수, int Նախընտրանքներ,
                 struct sockaddr *հասցե, socklen_t *հասցե_տեւողություն) {
    int 요청[2] = {(int)հասցե, (int)հասցե_տեւողություն};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)տվյալ, 바이트수, Նախընտրանքներ, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *հասցե, socklen_t *հասցե_տեւողություն) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)հասցե, (int)հասցե_տեւողություն, 0, 0));
}
int setsockopt(int 파일서술자, int շերտ_արժեք, int Կարգավորումներ_անուն, const void *արժեք, socklen_t արժեք_տեւողություն) {
    if (շերտ_արժեք != SOL_SOCKET || Կարգավորումներ_անուն != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!արժեք) { errno = EFAULT; return -1; }
    if (արժեք_տեւողություն != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = արժեք;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t արժեք) { return (արժեք << 8) | (արժեք >> 8); }
uint16_t ntohs(uint16_t արժեք) { return htons(արժեք); }
uint32_t htonl(uint32_t արժեք) {
    return (արժեք << 24) | ((արժեք << 8) & 0xff0000U) | ((արժեք >> 8) & 0xff00U) | (արժեք >> 24);
}
uint32_t ntohl(uint32_t արժեք) { return htonl(արժեք); }
int inet_pton(int 주소체계, const char *տող_արժեք_6ca8363c, void *հասցե) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!տող_արժեք_6ca8363c || !հասցե) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int փորակ_մուտքագրում = 0; փորակ_մուտքագրում < 4; փորակ_մուտքագրում++) {
        int արժեք = 0, 자릿수 = 0;
        const char *Գործարկել = տող_արժեք_6ca8363c;
        while (*տող_արժեք_6ca8363c >= '0' && *տող_արժեք_6ca8363c <= '9') {
            if (++자릿수 > 3) return 0;
            արժեք = արժեք * 10 + *տող_արժեք_6ca8363c++ - '0';
        }
        if (!자릿수 || արժեք > 255 || (자릿수 > 1 && *Գործարկել == '0')) return 0;
        임시[փորակ_մուտքագրում] = արժեք;
        if (փորակ_մուտքագրում < 3) { if (*տող_արժեք_6ca8363c++ != '.') return 0; }
        else if (*տող_արժեք_6ca8363c) return 0;
    }
    for (int փորակ_մուտքագրում = 0; փորակ_մուտքագրում < 4; փորակ_մուտքագրում++) ((unsigned char *)հասցե)[փորակ_մուտքագրում] = 임시[փորակ_մուտքագրում];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *հասցե, char *տող_արժեք_6ca8363c, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!հասցե || !տող_արժեք_6ca8363c) { errno = EFAULT; return 0; }
    const unsigned char *수 = հասցե;
    char 임시[16]; unsigned int տեւողություն_արժեք = 0;
    for (int փորակ_մուտքագրում = 0; փորակ_մուտքագրում < 4; փորակ_մուտքագրում++) {
        unsigned int արժեք = 수[փորակ_մուտքագրում];
        if (արժեք >= 100) 임시[տեւողություն_արժեք++] = '0' + արժեք / 100;
        if (արժեք >= 10) 임시[տեւողություն_արժեք++] = '0' + արժեք / 10 % 10;
        임시[տեւողություն_արժեք++] = '0' + արժեք % 10;
        if (փորակ_մուտքագրում < 3) 임시[տեւողություն_արժեք++] = '.';
    }
    임시[տեւողություն_արժեք++] = 0;
    if (용량 < տեւողություն_արժեք) { errno = ENOSPC; return 0; }
    for (unsigned int փորակ_մուտքագրում = 0; փորակ_մուտքագրում < տեւողություն_արժեք; փորակ_մուտքագրում++) տող_արժեք_6ca8363c[փորակ_մուտքագրում] = 임시[փորակ_մուտքագրում];
    return տող_արժեք_6ca8363c;
}
