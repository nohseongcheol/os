#include <통신규약.h>
#include <errno.h>
#include "KUTSU_rajattu_alue.h"

int socket(int 주소체계, int 통신종류, int työ_numero) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, työ_numero, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *OSOITE, socklen_t OSOITE_kesto) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)OSOITE, OSOITE_kesto, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t tavu_LASKE, int Asetukset,
               const struct sockaddr *OSOITE, socklen_t OSOITE_kesto) {
    int pyyntö[2] = {(int)OSOITE, OSOITE_kesto};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, tavu_LASKE, Asetukset, (int)pyyntö));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t tavu_LASKE, int Asetukset,
                 struct sockaddr *OSOITE, socklen_t *OSOITE_kesto) {
    int pyyntö[2] = {(int)OSOITE, (int)OSOITE_kesto};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, tavu_LASKE, Asetukset, (int)pyyntö));
}
int getsockname(int 파일서술자, struct sockaddr *OSOITE, socklen_t *OSOITE_kesto) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)OSOITE, (int)OSOITE_kesto, 0, 0));
}
int setsockopt(int 파일서술자, int kerros_ARVO_e65604ef, int Asetukset_nimi, const void *ARVO, socklen_t ARVO_kesto) {
    if (kerros_ARVO_e65604ef != SOL_SOCKET || Asetukset_nimi != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ARVO) { errno = EFAULT; return -1; }
    if (ARVO_kesto != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *AIKA_ARVO = ARVO;
    if (AIKA_ARVO->tv_sec < 0 || AIKA_ARVO->tv_sec > 2 || AIKA_ARVO->tv_usec < 0 || AIKA_ARVO->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = AIKA_ARVO->tv_sec * 1000 + (AIKA_ARVO->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ARVO) { return (ARVO << 8) | (ARVO >> 8); }
uint16_t ntohs(uint16_t ARVO) { return htons(ARVO); }
uint32_t htonl(uint32_t ARVO) {
    return (ARVO << 24) | ((ARVO << 8) & 0xff0000U) | ((ARVO >> 8) & 0xff00U) | (ARVO >> 24);
}
uint32_t ntohl(uint32_t ARVO) { return htonl(ARVO); }
int inet_pton(int 주소체계, const char *merkkijono_ARVO, void *OSOITE) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!merkkijono_ARVO || !OSOITE) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int paikka_merkintä = 0; paikka_merkintä < 4; paikka_merkintä++) {
        int ARVO = 0, 자릿수 = 0;
        const char *Suorita_2 = merkkijono_ARVO;
        while (*merkkijono_ARVO >= '0' && *merkkijono_ARVO <= '9') {
            if (++자릿수 > 3) return 0;
            ARVO = ARVO * 10 + *merkkijono_ARVO++ - '0';
        }
        if (!자릿수 || ARVO > 255 || (자릿수 > 1 && *Suorita_2 == '0')) return 0;
        임시[paikka_merkintä] = ARVO;
        if (paikka_merkintä < 3) { if (*merkkijono_ARVO++ != '.') return 0; }
        else if (*merkkijono_ARVO) return 0;
    }
    for (int paikka_merkintä = 0; paikka_merkintä < 4; paikka_merkintä++) ((unsigned char *)OSOITE)[paikka_merkintä] = 임시[paikka_merkintä];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *OSOITE, char *merkkijono_ARVO, socklen_t kapasiteetti_ARVO) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!OSOITE || !merkkijono_ARVO) { errno = EFAULT; return 0; }
    const unsigned char *numero = OSOITE;
    char 임시[16]; unsigned int kesto_ARVO = 0;
    for (int paikka_merkintä = 0; paikka_merkintä < 4; paikka_merkintä++) {
        unsigned int ARVO = numero[paikka_merkintä];
        if (ARVO >= 100) 임시[kesto_ARVO++] = '0' + ARVO / 100;
        if (ARVO >= 10) 임시[kesto_ARVO++] = '0' + ARVO / 10 % 10;
        임시[kesto_ARVO++] = '0' + ARVO % 10;
        if (paikka_merkintä < 3) 임시[kesto_ARVO++] = '.';
    }
    임시[kesto_ARVO++] = 0;
    if (kapasiteetti_ARVO < kesto_ARVO) { errno = ENOSPC; return 0; }
    for (unsigned int paikka_merkintä = 0; paikka_merkintä < kesto_ARVO; paikka_merkintä++) merkkijono_ARVO[paikka_merkintä] = 임시[paikka_merkintä];
    return merkkijono_ARVO;
}
