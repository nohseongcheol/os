#include <통신규약.h>
#include <errno.h>
#include "Ring_grense.h"

int socket(int 주소체계, int 통신종류, int sak_nummer) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, sak_nummer, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *e_post, socklen_t e_post_lengde) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)e_post, e_post_lengde, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t byte_ANTALL, int Innstillinger,
               const struct sockaddr *e_post, socklen_t e_post_lengde) {
    int forespørsel[2] = {(int)e_post, e_post_lengde};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, byte_ANTALL, Innstillinger, (int)forespørsel));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t byte_ANTALL, int Innstillinger,
                 struct sockaddr *e_post, socklen_t *e_post_lengde) {
    int forespørsel[2] = {(int)e_post, (int)e_post_lengde};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, byte_ANTALL, Innstillinger, (int)forespørsel));
}
int getsockname(int 파일서술자, struct sockaddr *e_post, socklen_t *e_post_lengde) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)e_post, (int)e_post_lengde, 0, 0));
}
int setsockopt(int 파일서술자, int lag_VERDI, int Innstillinger_navn, const void *VERDI, socklen_t VERDI_lengde) {
    if (lag_VERDI != SOL_SOCKET || Innstillinger_navn != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VERDI) { errno = EFAULT; return -1; }
    if (VERDI_lengde != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *TID_VERDI = VERDI;
    if (TID_VERDI->tv_sec < 0 || TID_VERDI->tv_sec > 2 || TID_VERDI->tv_usec < 0 || TID_VERDI->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = TID_VERDI->tv_sec * 1000 + (TID_VERDI->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VERDI) { return (VERDI << 8) | (VERDI >> 8); }
uint16_t ntohs(uint16_t VERDI) { return htons(VERDI); }
uint32_t htonl(uint32_t VERDI) {
    return (VERDI << 24) | ((VERDI << 8) & 0xff0000U) | ((VERDI >> 8) & 0xff00U) | (VERDI >> 24);
}
uint32_t ntohl(uint32_t VERDI) { return htonl(VERDI); }
int inet_pton(int 주소체계, const char *streng_VERDI, void *e_post) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!streng_VERDI || !e_post) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int åpning_oppføring = 0; åpning_oppføring < 4; åpning_oppføring++) {
        int VERDI = 0, 자릿수 = 0;
        const char *Kjør_2 = streng_VERDI;
        while (*streng_VERDI >= '0' && *streng_VERDI <= '9') {
            if (++자릿수 > 3) return 0;
            VERDI = VERDI * 10 + *streng_VERDI++ - '0';
        }
        if (!자릿수 || VERDI > 255 || (자릿수 > 1 && *Kjør_2 == '0')) return 0;
        임시[åpning_oppføring] = VERDI;
        if (åpning_oppføring < 3) { if (*streng_VERDI++ != '.') return 0; }
        else if (*streng_VERDI) return 0;
    }
    for (int åpning_oppføring = 0; åpning_oppføring < 4; åpning_oppføring++) ((unsigned char *)e_post)[åpning_oppføring] = 임시[åpning_oppføring];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *e_post, char *streng_VERDI, socklen_t kapasitet_VERDI) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!e_post || !streng_VERDI) { errno = EFAULT; return 0; }
    const unsigned char *nummer = e_post;
    char 임시[16]; unsigned int lengde_VERDI = 0;
    for (int åpning_oppføring = 0; åpning_oppføring < 4; åpning_oppføring++) {
        unsigned int VERDI = nummer[åpning_oppføring];
        if (VERDI >= 100) 임시[lengde_VERDI++] = '0' + VERDI / 100;
        if (VERDI >= 10) 임시[lengde_VERDI++] = '0' + VERDI / 10 % 10;
        임시[lengde_VERDI++] = '0' + VERDI % 10;
        if (åpning_oppføring < 3) 임시[lengde_VERDI++] = '.';
    }
    임시[lengde_VERDI++] = 0;
    if (kapasitet_VERDI < lengde_VERDI) { errno = ENOSPC; return 0; }
    for (unsigned int åpning_oppføring = 0; åpning_oppføring < lengde_VERDI; åpning_oppføring++) streng_VERDI[åpning_oppføring] = 임시[åpning_oppføring];
    return streng_VERDI;
}
