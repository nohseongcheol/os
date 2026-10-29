#include <síť_ABI.h>
#include <errno.h>
#include "VOLAT_mez.h"

int socket(int 주소체계, int síť_Druh, int případ_číslo) {
    return 호출결과(jkoros_syscall(41, 주소체계, síť_Druh, případ_číslo, 0, 0));
}
int bind(int Soubor_popisovač, const struct sockaddr *Adresa, socklen_t ODKAZ_délka) {
    return 호출결과(jkoros_syscall(42, Soubor_popisovač, (int)Adresa, ODKAZ_délka, 0, 0));
}
ssize_t sendto(int Soubor_popisovač, const void *data, size_t bajt_POČET, int Nastavení,
               const struct sockaddr *Adresa, socklen_t ODKAZ_délka) {
    int žádost[2] = {(int)Adresa, ODKAZ_délka};
    return 호출결과(jkoros_syscall(43, Soubor_popisovač, (int)data, bajt_POČET, Nastavení, (int)žádost));
}
ssize_t recvfrom(int Soubor_popisovač, void *data, size_t bajt_POČET, int Nastavení,
                 struct sockaddr *Adresa, socklen_t *ODKAZ_délka) {
    int žádost[2] = {(int)Adresa, (int)ODKAZ_délka};
    return 호출결과(jkoros_syscall(44, Soubor_popisovač, (int)data, bajt_POČET, Nastavení, (int)žádost));
}
int getsockname(int Soubor_popisovač, struct sockaddr *Adresa, socklen_t *ODKAZ_délka) {
    return 호출결과(jkoros_syscall(45, Soubor_popisovač, (int)Adresa, (int)ODKAZ_délka, 0, 0));
}
int setsockopt(int Soubor_popisovač, int vrstva_HODNOTA, int Nastavení_název, const void *HODNOTA, socklen_t HODNOTA_délka) {
    if (vrstva_HODNOTA != SOL_SOCKET || Nastavení_název != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!HODNOTA) { errno = EFAULT; return -1; }
    if (HODNOTA_délka != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *časová_hodnota = HODNOTA;
    if (časová_hodnota->tv_sec < 0 || časová_hodnota->tv_sec > 2 || časová_hodnota->tv_usec < 0 || časová_hodnota->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = časová_hodnota->tv_sec * 1000 + (časová_hodnota->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, Soubor_popisovač, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t HODNOTA) { return (HODNOTA << 8) | (HODNOTA >> 8); }
uint16_t ntohs(uint16_t HODNOTA) { return htons(HODNOTA); }
uint32_t htonl(uint32_t HODNOTA) {
    return (HODNOTA << 24) | ((HODNOTA << 8) & 0xff0000U) | ((HODNOTA >> 8) & 0xff00U) | (HODNOTA >> 24);
}
uint32_t ntohl(uint32_t HODNOTA) { return htonl(HODNOTA); }
int inet_pton(int 주소체계, const char *řetězec_HODNOTA, void *Adresa) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!řetězec_HODNOTA || !Adresa) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int přihrádka_položka = 0; přihrádka_položka < 4; přihrádka_položka++) {
        int HODNOTA = 0, 자릿수 = 0;
        const char *Spustit_2 = řetězec_HODNOTA;
        while (*řetězec_HODNOTA >= '0' && *řetězec_HODNOTA <= '9') {
            if (++자릿수 > 3) return 0;
            HODNOTA = HODNOTA * 10 + *řetězec_HODNOTA++ - '0';
        }
        if (!자릿수 || HODNOTA > 255 || (자릿수 > 1 && *Spustit_2 == '0')) return 0;
        임시[přihrádka_položka] = HODNOTA;
        if (přihrádka_položka < 3) { if (*řetězec_HODNOTA++ != '.') return 0; }
        else if (*řetězec_HODNOTA) return 0;
    }
    for (int přihrádka_položka = 0; přihrádka_položka < 4; přihrádka_položka++) ((unsigned char *)Adresa)[přihrádka_položka] = 임시[přihrádka_položka];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *Adresa, char *řetězec_HODNOTA, socklen_t kapacita_HODNOTA) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!Adresa || !řetězec_HODNOTA) { errno = EFAULT; return 0; }
    const unsigned char *číslo = Adresa;
    char 임시[16]; unsigned int délka_HODNOTA = 0;
    for (int přihrádka_položka = 0; přihrádka_položka < 4; přihrádka_položka++) {
        unsigned int HODNOTA = číslo[přihrádka_položka];
        if (HODNOTA >= 100) 임시[délka_HODNOTA++] = '0' + HODNOTA / 100;
        if (HODNOTA >= 10) 임시[délka_HODNOTA++] = '0' + HODNOTA / 10 % 10;
        임시[délka_HODNOTA++] = '0' + HODNOTA % 10;
        if (přihrádka_položka < 3) 임시[délka_HODNOTA++] = '.';
    }
    임시[délka_HODNOTA++] = 0;
    if (kapacita_HODNOTA < délka_HODNOTA) { errno = ENOSPC; return 0; }
    for (unsigned int přihrádka_položka = 0; přihrádka_položka < délka_HODNOTA; přihrádka_položka++) řetězec_HODNOTA[přihrádka_položka] = 임시[přihrádka_položka];
    return řetězec_HODNOTA;
}
