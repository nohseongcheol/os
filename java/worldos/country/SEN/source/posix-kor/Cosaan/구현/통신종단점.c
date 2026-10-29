#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *dëkkuwaay, socklen_t dëkkuwaay_diir) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)dëkkuwaay, dëkkuwaay_diir, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *mbir, size_t 바이트수, int Jekkal_yi,
               const struct sockaddr *dëkkuwaay, socklen_t dëkkuwaay_diir) {
    int 요청[2] = {(int)dëkkuwaay, dëkkuwaay_diir};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)mbir, 바이트수, Jekkal_yi, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *mbir, size_t 바이트수, int Jekkal_yi,
                 struct sockaddr *dëkkuwaay, socklen_t *dëkkuwaay_diir) {
    int 요청[2] = {(int)dëkkuwaay, (int)dëkkuwaay_diir};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)mbir, 바이트수, Jekkal_yi, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *dëkkuwaay, socklen_t *dëkkuwaay_diir) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)dëkkuwaay, (int)dëkkuwaay_diir, 0, 0));
}
int setsockopt(int 파일서술자, int déggoob_wet_xëyma, int Jekkal_yi_tur, const void *xëyma, socklen_t xëyma_diir) {
    if (déggoob_wet_xëyma != SOL_SOCKET || Jekkal_yi_tur != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!xëyma) { errno = EFAULT; return -1; }
    if (xëyma_diir != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = xëyma;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t xëyma) { return (xëyma << 8) | (xëyma >> 8); }
uint16_t ntohs(uint16_t xëyma) { return htons(xëyma); }
uint32_t htonl(uint32_t xëyma) {
    return (xëyma << 24) | ((xëyma << 8) & 0xff0000U) | ((xëyma >> 8) & 0xff00U) | (xëyma >> 24);
}
uint32_t ntohl(uint32_t xëyma) { return htonl(xëyma); }
int inet_pton(int 주소체계, const char *araf_yu_bennoo_xëyma, void *dëkkuwaay) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!araf_yu_bennoo_xëyma || !dëkkuwaay) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 4; xar_xar_dugal_xabaar++) {
        int xëyma = 0, 자릿수 = 0;
        const char *daw = araf_yu_bennoo_xëyma;
        while (*araf_yu_bennoo_xëyma >= '0' && *araf_yu_bennoo_xëyma <= '9') {
            if (++자릿수 > 3) return 0;
            xëyma = xëyma * 10 + *araf_yu_bennoo_xëyma++ - '0';
        }
        if (!자릿수 || xëyma > 255 || (자릿수 > 1 && *daw == '0')) return 0;
        임시[xar_xar_dugal_xabaar] = xëyma;
        if (xar_xar_dugal_xabaar < 3) { if (*araf_yu_bennoo_xëyma++ != '.') return 0; }
        else if (*araf_yu_bennoo_xëyma) return 0;
    }
    for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 4; xar_xar_dugal_xabaar++) ((unsigned char *)dëkkuwaay)[xar_xar_dugal_xabaar] = 임시[xar_xar_dugal_xabaar];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *dëkkuwaay, char *araf_yu_bennoo_xëyma, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!dëkkuwaay || !araf_yu_bennoo_xëyma) { errno = EFAULT; return 0; }
    const unsigned char *수 = dëkkuwaay;
    char 임시[16]; unsigned int diir_xëyma = 0;
    for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 4; xar_xar_dugal_xabaar++) {
        unsigned int xëyma = 수[xar_xar_dugal_xabaar];
        if (xëyma >= 100) 임시[diir_xëyma++] = '0' + xëyma / 100;
        if (xëyma >= 10) 임시[diir_xëyma++] = '0' + xëyma / 10 % 10;
        임시[diir_xëyma++] = '0' + xëyma % 10;
        if (xar_xar_dugal_xabaar < 3) 임시[diir_xëyma++] = '.';
    }
    임시[diir_xëyma++] = 0;
    if (용량 < diir_xëyma) { errno = ENOSPC; return 0; }
    for (unsigned int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < diir_xëyma; xar_xar_dugal_xabaar++) araf_yu_bennoo_xëyma[xar_xar_dugal_xabaar] = 임시[xar_xar_dugal_xabaar];
    return araf_yu_bennoo_xëyma;
}
