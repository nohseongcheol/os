#include <rede_ABI.h>
#include <errno.h>
#include "Ligar_limite.h"

int socket(int 주소체계, int rede_Tipo, int contrato_número) {
    return 호출결과(jkoros_syscall(41, 주소체계, rede_Tipo, contrato_número, 0, 0));
}
int bind(int Arquivo_descritor, const struct sockaddr *Endereço, socklen_t email_duração) {
    return 호출결과(jkoros_syscall(42, Arquivo_descritor, (int)Endereço, email_duração, 0, 0));
}
ssize_t sendto(int Arquivo_descritor, const void *dados, size_t byte_CONT_NÚM, int Definições,
               const struct sockaddr *Endereço, socklen_t email_duração) {
    int solicitação[2] = {(int)Endereço, email_duração};
    return 호출결과(jkoros_syscall(43, Arquivo_descritor, (int)dados, byte_CONT_NÚM, Definições, (int)solicitação));
}
ssize_t recvfrom(int Arquivo_descritor, void *dados, size_t byte_CONT_NÚM, int Definições,
                 struct sockaddr *Endereço, socklen_t *email_duração) {
    int solicitação[2] = {(int)Endereço, (int)email_duração};
    return 호출결과(jkoros_syscall(44, Arquivo_descritor, (int)dados, byte_CONT_NÚM, Definições, (int)solicitação));
}
int getsockname(int Arquivo_descritor, struct sockaddr *Endereço, socklen_t *email_duração) {
    return 호출결과(jkoros_syscall(45, Arquivo_descritor, (int)Endereço, (int)email_duração, 0, 0));
}
int setsockopt(int Arquivo_descritor, int camada_VALOR, int Configurações_nome, const void *VALOR, socklen_t VALOR_duração) {
    if (camada_VALOR != SOL_SOCKET || Configurações_nome != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALOR) { errno = EFAULT; return -1; }
    if (VALOR_duração != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *valor_temporal = VALOR;
    if (valor_temporal->tv_sec < 0 || valor_temporal->tv_sec > 2 || valor_temporal->tv_usec < 0 || valor_temporal->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = valor_temporal->tv_sec * 1000 + (valor_temporal->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, Arquivo_descritor, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VALOR) { return (VALOR << 8) | (VALOR >> 8); }
uint16_t ntohs(uint16_t VALOR) { return htons(VALOR); }
uint32_t htonl(uint32_t VALOR) {
    return (VALOR << 24) | ((VALOR << 8) & 0xff0000U) | ((VALOR >> 8) & 0xff00U) | (VALOR >> 24);
}
uint32_t ntohl(uint32_t VALOR) { return htonl(VALOR); }
int inet_pton(int 주소체계, const char *cadeia_VALOR, void *Endereço) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!cadeia_VALOR || !Endereço) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int slot_entrada = 0; slot_entrada < 4; slot_entrada++) {
        int VALOR = 0, 자릿수 = 0;
        const char *iniciar = cadeia_VALOR;
        while (*cadeia_VALOR >= '0' && *cadeia_VALOR <= '9') {
            if (++자릿수 > 3) return 0;
            VALOR = VALOR * 10 + *cadeia_VALOR++ - '0';
        }
        if (!자릿수 || VALOR > 255 || (자릿수 > 1 && *iniciar == '0')) return 0;
        임시[slot_entrada] = VALOR;
        if (slot_entrada < 3) { if (*cadeia_VALOR++ != '.') return 0; }
        else if (*cadeia_VALOR) return 0;
    }
    for (int slot_entrada = 0; slot_entrada < 4; slot_entrada++) ((unsigned char *)Endereço)[slot_entrada] = 임시[slot_entrada];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *Endereço, char *cadeia_VALOR, socklen_t capacidade_VALOR) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!Endereço || !cadeia_VALOR) { errno = EFAULT; return 0; }
    const unsigned char *número = Endereço;
    char 임시[16]; unsigned int duração_VALOR = 0;
    for (int slot_entrada = 0; slot_entrada < 4; slot_entrada++) {
        unsigned int VALOR = número[slot_entrada];
        if (VALOR >= 100) 임시[duração_VALOR++] = '0' + VALOR / 100;
        if (VALOR >= 10) 임시[duração_VALOR++] = '0' + VALOR / 10 % 10;
        임시[duração_VALOR++] = '0' + VALOR % 10;
        if (slot_entrada < 3) 임시[duração_VALOR++] = '.';
    }
    임시[duração_VALOR++] = 0;
    if (capacidade_VALOR < duração_VALOR) { errno = ENOSPC; return 0; }
    for (unsigned int slot_entrada = 0; slot_entrada < duração_VALOR; slot_entrada++) cadeia_VALOR[slot_entrada] = 임시[slot_entrada];
    return cadeia_VALOR;
}
