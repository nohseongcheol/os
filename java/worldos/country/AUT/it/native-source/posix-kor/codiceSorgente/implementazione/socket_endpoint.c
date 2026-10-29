#include <rete_ABI.h>
#include <errno.h>
#include "Chiama_limite.h"

int socket(int 주소체계, int rete_Kind, int caso_numero) {
    return 호출결과(jkoros_syscall(41, 주소체계, rete_Kind, caso_numero, 0, 0));
}
int bind(int File_descrittore, const struct sockaddr *e_mail, socklen_t e_mail_durata) {
    return 호출결과(jkoros_syscall(42, File_descrittore, (int)e_mail, e_mail_durata, 0, 0));
}
ssize_t sendto(int File_descrittore, const void *dati, size_t byte_CONTA_NUMERI, int Impostazioni,
               const struct sockaddr *e_mail, socklen_t e_mail_durata) {
    int richiesta[2] = {(int)e_mail, e_mail_durata};
    return 호출결과(jkoros_syscall(43, File_descrittore, (int)dati, byte_CONTA_NUMERI, Impostazioni, (int)richiesta));
}
ssize_t recvfrom(int File_descrittore, void *dati, size_t byte_CONTA_NUMERI, int Impostazioni,
                 struct sockaddr *e_mail, socklen_t *e_mail_durata) {
    int richiesta[2] = {(int)e_mail, (int)e_mail_durata};
    return 호출결과(jkoros_syscall(44, File_descrittore, (int)dati, byte_CONTA_NUMERI, Impostazioni, (int)richiesta));
}
int getsockname(int File_descrittore, struct sockaddr *e_mail, socklen_t *e_mail_durata) {
    return 호출결과(jkoros_syscall(45, File_descrittore, (int)e_mail, (int)e_mail_durata, 0, 0));
}
int setsockopt(int File_descrittore, int layer_VALORE, int Impostazioni_nome, const void *VALORE, socklen_t VALORE_durata) {
    if (layer_VALORE != SOL_SOCKET || Impostazioni_nome != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALORE) { errno = EFAULT; return -1; }
    if (VALORE_durata != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *valore = VALORE;
    if (valore->tv_sec < 0 || valore->tv_sec > 2 || valore->tv_usec < 0 || valore->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = valore->tv_sec * 1000 + (valore->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, File_descrittore, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VALORE) { return (VALORE << 8) | (VALORE >> 8); }
uint16_t ntohs(uint16_t VALORE) { return htons(VALORE); }
uint32_t htonl(uint32_t VALORE) {
    return (VALORE << 24) | ((VALORE << 8) & 0xff0000U) | ((VALORE >> 8) & 0xff00U) | (VALORE >> 24);
}
uint32_t ntohl(uint32_t VALORE) { return htonl(VALORE); }
int inet_pton(int 주소체계, const char *stringa_VALORE, void *e_mail) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!stringa_VALORE || !e_mail) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int slot_voce = 0; slot_voce < 4; slot_voce++) {
        int VALORE = 0, 자릿수 = 0;
        const char *avvia = stringa_VALORE;
        while (*stringa_VALORE >= '0' && *stringa_VALORE <= '9') {
            if (++자릿수 > 3) return 0;
            VALORE = VALORE * 10 + *stringa_VALORE++ - '0';
        }
        if (!자릿수 || VALORE > 255 || (자릿수 > 1 && *avvia == '0')) return 0;
        임시[slot_voce] = VALORE;
        if (slot_voce < 3) { if (*stringa_VALORE++ != '.') return 0; }
        else if (*stringa_VALORE) return 0;
    }
    for (int slot_voce = 0; slot_voce < 4; slot_voce++) ((unsigned char *)e_mail)[slot_voce] = 임시[slot_voce];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *e_mail, char *stringa_VALORE, socklen_t capacità_VALORE) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!e_mail || !stringa_VALORE) { errno = EFAULT; return 0; }
    const unsigned char *numero = e_mail;
    char 임시[16]; unsigned int durata_VALORE = 0;
    for (int slot_voce = 0; slot_voce < 4; slot_voce++) {
        unsigned int VALORE = numero[slot_voce];
        if (VALORE >= 100) 임시[durata_VALORE++] = '0' + VALORE / 100;
        if (VALORE >= 10) 임시[durata_VALORE++] = '0' + VALORE / 10 % 10;
        임시[durata_VALORE++] = '0' + VALORE % 10;
        if (slot_voce < 3) 임시[durata_VALORE++] = '.';
    }
    임시[durata_VALORE++] = 0;
    if (capacità_VALORE < durata_VALORE) { errno = ENOSPC; return 0; }
    for (unsigned int slot_voce = 0; slot_voce < durata_VALORE; slot_voce++) stringa_VALORE[slot_voce] = 임시[slot_voce];
    return stringa_VALORE;
}
