#include <통신규약.h>
#include <errno.h>
#include "KALD_grænse.h"

int socket(int 주소체계, int 통신종류, int job_tal) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, job_tal, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *mail, socklen_t mail_varighed) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)mail, mail_varighed, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t byte_TÆL, int Indstillinger,
               const struct sockaddr *mail, socklen_t mail_varighed) {
    int anmodning[2] = {(int)mail, mail_varighed};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, byte_TÆL, Indstillinger, (int)anmodning));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t byte_TÆL, int Indstillinger,
                 struct sockaddr *mail, socklen_t *mail_varighed) {
    int anmodning[2] = {(int)mail, (int)mail_varighed};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, byte_TÆL, Indstillinger, (int)anmodning));
}
int getsockname(int 파일서술자, struct sockaddr *mail, socklen_t *mail_varighed) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)mail, (int)mail_varighed, 0, 0));
}
int setsockopt(int 파일서술자, int lag_VÆRDI, int Indstillinger_navn, const void *VÆRDI, socklen_t VÆRDI_varighed) {
    if (lag_VÆRDI != SOL_SOCKET || Indstillinger_navn != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VÆRDI) { errno = EFAULT; return -1; }
    if (VÆRDI_varighed != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *TID_VÆRDI = VÆRDI;
    if (TID_VÆRDI->tv_sec < 0 || TID_VÆRDI->tv_sec > 2 || TID_VÆRDI->tv_usec < 0 || TID_VÆRDI->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = TID_VÆRDI->tv_sec * 1000 + (TID_VÆRDI->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VÆRDI) { return (VÆRDI << 8) | (VÆRDI >> 8); }
uint16_t ntohs(uint16_t VÆRDI) { return htons(VÆRDI); }
uint32_t htonl(uint32_t VÆRDI) {
    return (VÆRDI << 24) | ((VÆRDI << 8) & 0xff0000U) | ((VÆRDI >> 8) & 0xff00U) | (VÆRDI >> 24);
}
uint32_t ntohl(uint32_t VÆRDI) { return htonl(VÆRDI); }
int inet_pton(int 주소체계, const char *streng_VÆRDI, void *mail) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!streng_VÆRDI || !mail) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int udvidelsesstik_post = 0; udvidelsesstik_post < 4; udvidelsesstik_post++) {
        int VÆRDI = 0, 자릿수 = 0;
        const char *Kør_2 = streng_VÆRDI;
        while (*streng_VÆRDI >= '0' && *streng_VÆRDI <= '9') {
            if (++자릿수 > 3) return 0;
            VÆRDI = VÆRDI * 10 + *streng_VÆRDI++ - '0';
        }
        if (!자릿수 || VÆRDI > 255 || (자릿수 > 1 && *Kør_2 == '0')) return 0;
        임시[udvidelsesstik_post] = VÆRDI;
        if (udvidelsesstik_post < 3) { if (*streng_VÆRDI++ != '.') return 0; }
        else if (*streng_VÆRDI) return 0;
    }
    for (int udvidelsesstik_post = 0; udvidelsesstik_post < 4; udvidelsesstik_post++) ((unsigned char *)mail)[udvidelsesstik_post] = 임시[udvidelsesstik_post];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *mail, char *streng_VÆRDI, socklen_t kapacitet_VÆRDI) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!mail || !streng_VÆRDI) { errno = EFAULT; return 0; }
    const unsigned char *tal = mail;
    char 임시[16]; unsigned int varighed_VÆRDI = 0;
    for (int udvidelsesstik_post = 0; udvidelsesstik_post < 4; udvidelsesstik_post++) {
        unsigned int VÆRDI = tal[udvidelsesstik_post];
        if (VÆRDI >= 100) 임시[varighed_VÆRDI++] = '0' + VÆRDI / 100;
        if (VÆRDI >= 10) 임시[varighed_VÆRDI++] = '0' + VÆRDI / 10 % 10;
        임시[varighed_VÆRDI++] = '0' + VÆRDI % 10;
        if (udvidelsesstik_post < 3) 임시[varighed_VÆRDI++] = '.';
    }
    임시[varighed_VÆRDI++] = 0;
    if (kapacitet_VÆRDI < varighed_VÆRDI) { errno = ENOSPC; return 0; }
    for (unsigned int udvidelsesstik_post = 0; udvidelsesstik_post < varighed_VÆRDI; udvidelsesstik_post++) streng_VÆRDI[udvidelsesstik_post] = 임시[udvidelsesstik_post];
    return streng_VÆRDI;
}
