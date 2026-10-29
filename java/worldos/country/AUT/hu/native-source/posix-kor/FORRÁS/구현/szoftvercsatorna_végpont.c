#include <통신규약.h>
#include <errno.h>
#include "hív_határ.h"

int socket(int 주소체계, int hálózat_Altípus, int eset_szám) {
    return 호출결과(jkoros_syscall(41, 주소체계, hálózat_Altípus, eset_szám, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *CÍM, socklen_t CÍM_hossz) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)CÍM, CÍM_hossz, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *adat, size_t bájt_DARAB, int Beállítások,
               const struct sockaddr *CÍM, socklen_t CÍM_hossz) {
    int kérés[2] = {(int)CÍM, CÍM_hossz};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)adat, bájt_DARAB, Beállítások, (int)kérés));
}
ssize_t recvfrom(int 파일서술자, void *adat, size_t bájt_DARAB, int Beállítások,
                 struct sockaddr *CÍM, socklen_t *CÍM_hossz) {
    int kérés[2] = {(int)CÍM, (int)CÍM_hossz};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)adat, bájt_DARAB, Beállítások, (int)kérés));
}
int getsockname(int 파일서술자, struct sockaddr *CÍM, socklen_t *CÍM_hossz) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)CÍM, (int)CÍM_hossz, 0, 0));
}
int setsockopt(int 파일서술자, int réteg_ÉRTÉK, int Gépház_név, const void *ÉRTÉK, socklen_t ÉRTÉK_hossz) {
    if (réteg_ÉRTÉK != SOL_SOCKET || Gépház_név != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ÉRTÉK) { errno = EFAULT; return -1; }
    if (ÉRTÉK_hossz != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *IDŐ_ÉRTÉK = ÉRTÉK;
    if (IDŐ_ÉRTÉK->tv_sec < 0 || IDŐ_ÉRTÉK->tv_sec > 2 || IDŐ_ÉRTÉK->tv_usec < 0 || IDŐ_ÉRTÉK->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = IDŐ_ÉRTÉK->tv_sec * 1000 + (IDŐ_ÉRTÉK->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ÉRTÉK) { return (ÉRTÉK << 8) | (ÉRTÉK >> 8); }
uint16_t ntohs(uint16_t ÉRTÉK) { return htons(ÉRTÉK); }
uint32_t htonl(uint32_t ÉRTÉK) {
    return (ÉRTÉK << 24) | ((ÉRTÉK << 8) & 0xff0000U) | ((ÉRTÉK >> 8) & 0xff00U) | (ÉRTÉK >> 24);
}
uint32_t ntohl(uint32_t ÉRTÉK) { return htonl(ÉRTÉK); }
int inet_pton(int 주소체계, const char *sztring_ÉRTÉK, void *CÍM) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!sztring_ÉRTÉK || !CÍM) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 4; tárolóhely_bejegyzés++) {
        int ÉRTÉK = 0, 자릿수 = 0;
        const char *Futtatás = sztring_ÉRTÉK;
        while (*sztring_ÉRTÉK >= '0' && *sztring_ÉRTÉK <= '9') {
            if (++자릿수 > 3) return 0;
            ÉRTÉK = ÉRTÉK * 10 + *sztring_ÉRTÉK++ - '0';
        }
        if (!자릿수 || ÉRTÉK > 255 || (자릿수 > 1 && *Futtatás == '0')) return 0;
        임시[tárolóhely_bejegyzés] = ÉRTÉK;
        if (tárolóhely_bejegyzés < 3) { if (*sztring_ÉRTÉK++ != '.') return 0; }
        else if (*sztring_ÉRTÉK) return 0;
    }
    for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 4; tárolóhely_bejegyzés++) ((unsigned char *)CÍM)[tárolóhely_bejegyzés] = 임시[tárolóhely_bejegyzés];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *CÍM, char *sztring_ÉRTÉK, socklen_t kapacitás_ÉRTÉK) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!CÍM || !sztring_ÉRTÉK) { errno = EFAULT; return 0; }
    const unsigned char *szám = CÍM;
    char 임시[16]; unsigned int hossz_ÉRTÉK = 0;
    for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 4; tárolóhely_bejegyzés++) {
        unsigned int ÉRTÉK = szám[tárolóhely_bejegyzés];
        if (ÉRTÉK >= 100) 임시[hossz_ÉRTÉK++] = '0' + ÉRTÉK / 100;
        if (ÉRTÉK >= 10) 임시[hossz_ÉRTÉK++] = '0' + ÉRTÉK / 10 % 10;
        임시[hossz_ÉRTÉK++] = '0' + ÉRTÉK % 10;
        if (tárolóhely_bejegyzés < 3) 임시[hossz_ÉRTÉK++] = '.';
    }
    임시[hossz_ÉRTÉK++] = 0;
    if (kapacitás_ÉRTÉK < hossz_ÉRTÉK) { errno = ENOSPC; return 0; }
    for (unsigned int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < hossz_ÉRTÉK; tárolóhely_bejegyzés++) sztring_ÉRTÉK[tárolóhely_bejegyzés] = 임시[tárolóhely_bejegyzés];
    return sztring_ÉRTÉK;
}
