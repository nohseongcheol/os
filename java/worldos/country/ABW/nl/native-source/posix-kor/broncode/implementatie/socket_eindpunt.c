#include <통신규약.h>
#include <errno.h>
#include "Bellen_grens.h"

int socket(int 주소체계, int net_soort, int taak_nummer) {
    return 호출결과(jkoros_syscall(41, 주소체계, net_soort, taak_nummer, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ADRES, socklen_t ADRES_tijdsduur) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ADRES, ADRES_tijdsduur, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *gegevens, size_t byte_AANTAL, int Instellingen,
               const struct sockaddr *ADRES, socklen_t ADRES_tijdsduur) {
    int aanvraag[2] = {(int)ADRES, ADRES_tijdsduur};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)gegevens, byte_AANTAL, Instellingen, (int)aanvraag));
}
ssize_t recvfrom(int 파일서술자, void *gegevens, size_t byte_AANTAL, int Instellingen,
                 struct sockaddr *ADRES, socklen_t *ADRES_tijdsduur) {
    int aanvraag[2] = {(int)ADRES, (int)ADRES_tijdsduur};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)gegevens, byte_AANTAL, Instellingen, (int)aanvraag));
}
int getsockname(int 파일서술자, struct sockaddr *ADRES, socklen_t *ADRES_tijdsduur) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ADRES, (int)ADRES_tijdsduur, 0, 0));
}
int setsockopt(int 파일서술자, int laag_WAARDE, int Instellingen_naam, const void *WAARDE, socklen_t WAARDE_tijdsduur) {
    if (laag_WAARDE != SOL_SOCKET || Instellingen_naam != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!WAARDE) { errno = EFAULT; return -1; }
    if (WAARDE_tijdsduur != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *TIJD_WAARDE = WAARDE;
    if (TIJD_WAARDE->tv_sec < 0 || TIJD_WAARDE->tv_sec > 2 || TIJD_WAARDE->tv_usec < 0 || TIJD_WAARDE->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = TIJD_WAARDE->tv_sec * 1000 + (TIJD_WAARDE->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t WAARDE) { return (WAARDE << 8) | (WAARDE >> 8); }
uint16_t ntohs(uint16_t WAARDE) { return htons(WAARDE); }
uint32_t htonl(uint32_t WAARDE) {
    return (WAARDE << 24) | ((WAARDE << 8) & 0xff0000U) | ((WAARDE >> 8) & 0xff00U) | (WAARDE >> 24);
}
uint32_t ntohl(uint32_t WAARDE) { return htonl(WAARDE); }
int inet_pton(int 주소체계, const char *tekenreeks_WAARDE, void *ADRES) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!tekenreeks_WAARDE || !ADRES) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int sleuf_invoer = 0; sleuf_invoer < 4; sleuf_invoer++) {
        int WAARDE = 0, 자릿수 = 0;
        const char *starten = tekenreeks_WAARDE;
        while (*tekenreeks_WAARDE >= '0' && *tekenreeks_WAARDE <= '9') {
            if (++자릿수 > 3) return 0;
            WAARDE = WAARDE * 10 + *tekenreeks_WAARDE++ - '0';
        }
        if (!자릿수 || WAARDE > 255 || (자릿수 > 1 && *starten == '0')) return 0;
        임시[sleuf_invoer] = WAARDE;
        if (sleuf_invoer < 3) { if (*tekenreeks_WAARDE++ != '.') return 0; }
        else if (*tekenreeks_WAARDE) return 0;
    }
    for (int sleuf_invoer = 0; sleuf_invoer < 4; sleuf_invoer++) ((unsigned char *)ADRES)[sleuf_invoer] = 임시[sleuf_invoer];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ADRES, char *tekenreeks_WAARDE, socklen_t capaciteit_WAARDE) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ADRES || !tekenreeks_WAARDE) { errno = EFAULT; return 0; }
    const unsigned char *nummer = ADRES;
    char 임시[16]; unsigned int tijdsduur_WAARDE = 0;
    for (int sleuf_invoer = 0; sleuf_invoer < 4; sleuf_invoer++) {
        unsigned int WAARDE = nummer[sleuf_invoer];
        if (WAARDE >= 100) 임시[tijdsduur_WAARDE++] = '0' + WAARDE / 100;
        if (WAARDE >= 10) 임시[tijdsduur_WAARDE++] = '0' + WAARDE / 10 % 10;
        임시[tijdsduur_WAARDE++] = '0' + WAARDE % 10;
        if (sleuf_invoer < 3) 임시[tijdsduur_WAARDE++] = '.';
    }
    임시[tijdsduur_WAARDE++] = 0;
    if (capaciteit_WAARDE < tijdsduur_WAARDE) { errno = ENOSPC; return 0; }
    for (unsigned int sleuf_invoer = 0; sleuf_invoer < tijdsduur_WAARDE; sleuf_invoer++) tekenreeks_WAARDE[sleuf_invoer] = 임시[sleuf_invoer];
    return tekenreeks_WAARDE;
}
