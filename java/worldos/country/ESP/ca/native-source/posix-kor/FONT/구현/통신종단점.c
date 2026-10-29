#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *Adreça, socklen_t ADREÇA_durada) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)Adreça, ADREÇA_durada, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *dades, size_t byte_COMPT, int Ajusts,
               const struct sockaddr *Adreça, socklen_t ADREÇA_durada) {
    int sol_licitud[2] = {(int)Adreça, ADREÇA_durada};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)dades, byte_COMPT, Ajusts, (int)sol_licitud));
}
ssize_t recvfrom(int 파일서술자, void *dades, size_t byte_COMPT, int Ajusts,
                 struct sockaddr *Adreça, socklen_t *ADREÇA_durada) {
    int sol_licitud[2] = {(int)Adreça, (int)ADREÇA_durada};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)dades, byte_COMPT, Ajusts, (int)sol_licitud));
}
int getsockname(int 파일서술자, struct sockaddr *Adreça, socklen_t *ADREÇA_durada) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)Adreça, (int)ADREÇA_durada, 0, 0));
}
int setsockopt(int 파일서술자, int capa_VALOR, int Configuració_nom, const void *VALOR, socklen_t VALOR_durada) {
    if (capa_VALOR != SOL_SOCKET || Configuració_nom != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALOR) { errno = EFAULT; return -1; }
    if (VALOR_durada != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *Hora_VALOR = VALOR;
    if (Hora_VALOR->tv_sec < 0 || Hora_VALOR->tv_sec > 2 || Hora_VALOR->tv_usec < 0 || Hora_VALOR->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = Hora_VALOR->tv_sec * 1000 + (Hora_VALOR->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VALOR) { return (VALOR << 8) | (VALOR >> 8); }
uint16_t ntohs(uint16_t VALOR) { return htons(VALOR); }
uint32_t htonl(uint32_t VALOR) {
    return (VALOR << 24) | ((VALOR << 8) & 0xff0000U) | ((VALOR >> 8) & 0xff00U) | (VALOR >> 24);
}
uint32_t ntohl(uint32_t VALOR) { return htonl(VALOR); }
int inet_pton(int 주소체계, const char *cadena_VALOR, void *Adreça) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!cadena_VALOR || !Adreça) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int VALOR = 0, 자릿수 = 0;
        const char *Executa_2 = cadena_VALOR;
        while (*cadena_VALOR >= '0' && *cadena_VALOR <= '9') {
            if (++자릿수 > 3) return 0;
            VALOR = VALOR * 10 + *cadena_VALOR++ - '0';
        }
        if (!자릿수 || VALOR > 255 || (자릿수 > 1 && *Executa_2 == '0')) return 0;
        임시[칸] = VALOR;
        if (칸 < 3) { if (*cadena_VALOR++ != '.') return 0; }
        else if (*cadena_VALOR) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)Adreça)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *Adreça, char *cadena_VALOR, socklen_t capacitat_VALOR) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!Adreça || !cadena_VALOR) { errno = EFAULT; return 0; }
    const unsigned char *수 = Adreça;
    char 임시[16]; unsigned int durada_VALOR = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int VALOR = 수[칸];
        if (VALOR >= 100) 임시[durada_VALOR++] = '0' + VALOR / 100;
        if (VALOR >= 10) 임시[durada_VALOR++] = '0' + VALOR / 10 % 10;
        임시[durada_VALOR++] = '0' + VALOR % 10;
        if (칸 < 3) 임시[durada_VALOR++] = '.';
    }
    임시[durada_VALOR++] = 0;
    if (capacitat_VALOR < durada_VALOR) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < durada_VALOR; 칸++) cadena_VALOR[칸] = 임시[칸];
    return cadena_VALOR;
}
