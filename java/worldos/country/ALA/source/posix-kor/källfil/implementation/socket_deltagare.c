#include <통신규약.h>
#include <errno.h>
#include "ring_gräns.h"

int socket(int 주소체계, int nätverk_variant, int jobb_nummer) {
    return 호출결과(jkoros_syscall(41, 주소체계, nätverk_variant, jobb_nummer, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *Adress, socklen_t ADRESS_längd) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)Adress, ADRESS_längd, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t byte_ANTAL, int Inställningar,
               const struct sockaddr *Adress, socklen_t ADRESS_längd) {
    int begäran[2] = {(int)Adress, ADRESS_längd};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, byte_ANTAL, Inställningar, (int)begäran));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t byte_ANTAL, int Inställningar,
                 struct sockaddr *Adress, socklen_t *ADRESS_längd) {
    int begäran[2] = {(int)Adress, (int)ADRESS_längd};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, byte_ANTAL, Inställningar, (int)begäran));
}
int getsockname(int 파일서술자, struct sockaddr *Adress, socklen_t *ADRESS_längd) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)Adress, (int)ADRESS_längd, 0, 0));
}
int setsockopt(int 파일서술자, int nivå_värde, int Inställningar_namn, const void *värde, socklen_t värde_längd) {
    if (nivå_värde != SOL_SOCKET || Inställningar_namn != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!värde) { errno = EFAULT; return -1; }
    if (värde_längd != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *tid_värde = värde;
    if (tid_värde->tv_sec < 0 || tid_värde->tv_sec > 2 || tid_värde->tv_usec < 0 || tid_värde->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = tid_värde->tv_sec * 1000 + (tid_värde->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t värde) { return (värde << 8) | (värde >> 8); }
uint16_t ntohs(uint16_t värde) { return htons(värde); }
uint32_t htonl(uint32_t värde) {
    return (värde << 24) | ((värde << 8) & 0xff0000U) | ((värde >> 8) & 0xff00U) | (värde >> 24);
}
uint32_t ntohl(uint32_t värde) { return htonl(värde); }
int inet_pton(int 주소체계, const char *sträng_värde, void *Adress) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!sträng_värde || !Adress) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int fack_post = 0; fack_post < 4; fack_post++) {
        int värde = 0, 자릿수 = 0;
        const char *Kör = sträng_värde;
        while (*sträng_värde >= '0' && *sträng_värde <= '9') {
            if (++자릿수 > 3) return 0;
            värde = värde * 10 + *sträng_värde++ - '0';
        }
        if (!자릿수 || värde > 255 || (자릿수 > 1 && *Kör == '0')) return 0;
        임시[fack_post] = värde;
        if (fack_post < 3) { if (*sträng_värde++ != '.') return 0; }
        else if (*sträng_värde) return 0;
    }
    for (int fack_post = 0; fack_post < 4; fack_post++) ((unsigned char *)Adress)[fack_post] = 임시[fack_post];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *Adress, char *sträng_värde, socklen_t kapacitet_värde) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!Adress || !sträng_värde) { errno = EFAULT; return 0; }
    const unsigned char *nummer = Adress;
    char 임시[16]; unsigned int längd_värde = 0;
    for (int fack_post = 0; fack_post < 4; fack_post++) {
        unsigned int värde = nummer[fack_post];
        if (värde >= 100) 임시[längd_värde++] = '0' + värde / 100;
        if (värde >= 10) 임시[längd_värde++] = '0' + värde / 10 % 10;
        임시[längd_värde++] = '0' + värde % 10;
        if (fack_post < 3) 임시[längd_värde++] = '.';
    }
    임시[längd_värde++] = 0;
    if (kapacitet_värde < längd_värde) { errno = ENOSPC; return 0; }
    for (unsigned int fack_post = 0; fack_post < längd_värde; fack_post++) sträng_värde[fack_post] = 임시[fack_post];
    return sträng_värde;
}
