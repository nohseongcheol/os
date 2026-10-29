#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ikheli, socklen_t ikheli_ubude) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ikheli, ikheli_ubude, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *imininingwane, size_t 바이트수, int Izinhlelo,
               const struct sockaddr *ikheli, socklen_t ikheli_ubude) {
    int 요청[2] = {(int)ikheli, ikheli_ubude};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)imininingwane, 바이트수, Izinhlelo, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *imininingwane, size_t 바이트수, int Izinhlelo,
                 struct sockaddr *ikheli, socklen_t *ikheli_ubude) {
    int 요청[2] = {(int)ikheli, (int)ikheli_ubude};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)imininingwane, 바이트수, Izinhlelo, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ikheli, socklen_t *ikheli_ubude) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ikheli, (int)ikheli_ubude, 0, 0));
}
int setsockopt(int 파일서술자, int ugqinsi_inani, int Amasethingi_igama, const void *inani, socklen_t inani_ubude) {
    if (ugqinsi_inani != SOL_SOCKET || Amasethingi_igama != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!inani) { errno = EFAULT; return -1; }
    if (inani_ubude != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = inani;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t inani) { return (inani << 8) | (inani >> 8); }
uint16_t ntohs(uint16_t inani) { return htons(inani); }
uint32_t htonl(uint32_t inani) {
    return (inani << 24) | ((inani << 8) & 0xff0000U) | ((inani >> 8) & 0xff00U) | (inani >> 24);
}
uint32_t ntohl(uint32_t inani) { return htonl(inani); }
int inet_pton(int 주소체계, const char *uchunge_inani, void *ikheli) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!uchunge_inani || !ikheli) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 4; isikhala_okufakwayo++) {
        int inani = 0, 자릿수 = 0;
        const char *Sebenzisa = uchunge_inani;
        while (*uchunge_inani >= '0' && *uchunge_inani <= '9') {
            if (++자릿수 > 3) return 0;
            inani = inani * 10 + *uchunge_inani++ - '0';
        }
        if (!자릿수 || inani > 255 || (자릿수 > 1 && *Sebenzisa == '0')) return 0;
        임시[isikhala_okufakwayo] = inani;
        if (isikhala_okufakwayo < 3) { if (*uchunge_inani++ != '.') return 0; }
        else if (*uchunge_inani) return 0;
    }
    for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 4; isikhala_okufakwayo++) ((unsigned char *)ikheli)[isikhala_okufakwayo] = 임시[isikhala_okufakwayo];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ikheli, char *uchunge_inani, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ikheli || !uchunge_inani) { errno = EFAULT; return 0; }
    const unsigned char *수 = ikheli;
    char 임시[16]; unsigned int ubude_inani = 0;
    for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 4; isikhala_okufakwayo++) {
        unsigned int inani = 수[isikhala_okufakwayo];
        if (inani >= 100) 임시[ubude_inani++] = '0' + inani / 100;
        if (inani >= 10) 임시[ubude_inani++] = '0' + inani / 10 % 10;
        임시[ubude_inani++] = '0' + inani % 10;
        if (isikhala_okufakwayo < 3) 임시[ubude_inani++] = '.';
    }
    임시[ubude_inani++] = 0;
    if (용량 < ubude_inani) { errno = ENOSPC; return 0; }
    for (unsigned int isikhala_okufakwayo = 0; isikhala_okufakwayo < ubude_inani; isikhala_okufakwayo++) uchunge_inani[isikhala_okufakwayo] = 임시[isikhala_okufakwayo];
    return uchunge_inani;
}
