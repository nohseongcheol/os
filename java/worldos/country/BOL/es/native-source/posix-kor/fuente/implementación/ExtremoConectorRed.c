#include <ABIRed.h>
#include <errno.h>
#include "FronteraLlamada.h"

int socket(int esquemaDirección, int claseTipoRed, int númeroContrato) {
    return resultadoInvocación(jkoros_syscall(41, esquemaDirección, claseTipoRed, númeroContrato, 0, 0));
}
int bind(int descriptorArchivo, const struct sockaddr *dirección, socklen_t longitudDirección) {
    return resultadoInvocación(jkoros_syscall(42, descriptorArchivo, (int)dirección, longitudDirección, 0, 0));
}
ssize_t sendto(int descriptorArchivo, const void *Datos, size_t númeroElementosByte, int ajustes,
               const struct sockaddr *dirección, socklen_t longitudDirección) {
    int petición[2] = {(int)dirección, longitudDirección};
    return resultadoInvocación(jkoros_syscall(43, descriptorArchivo, (int)Datos, númeroElementosByte, ajustes, (int)petición));
}
ssize_t recvfrom(int descriptorArchivo, void *Datos, size_t númeroElementosByte, int ajustes,
                 struct sockaddr *dirección, socklen_t *longitudDirección) {
    int petición[2] = {(int)dirección, (int)longitudDirección};
    return resultadoInvocación(jkoros_syscall(44, descriptorArchivo, (int)Datos, númeroElementosByte, ajustes, (int)petición));
}
int getsockname(int descriptorArchivo, struct sockaddr *dirección, socklen_t *longitudDirección) {
    return resultadoInvocación(jkoros_syscall(45, descriptorArchivo, (int)dirección, (int)longitudDirección, 0, 0));
}
int setsockopt(int descriptorArchivo, int valorCapa, int nombreAjustes, const void *valor, socklen_t longitudValor) {
    if (valorCapa != SOL_SOCKET || nombreAjustes != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!valor) { errno = EFAULT; return -1; }
    if (longitudValor != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *valorTiempo = valor;
    if (valorTiempo->tv_sec < 0 || valorTiempo->tv_sec > 2 || valorTiempo->tv_usec < 0 || valorTiempo->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int milisegundos = valorTiempo->tv_sec * 1000 + (valorTiempo->tv_usec + 999) / 1000;
    return resultadoInvocación(jkoros_syscall(46, descriptorArchivo, milisegundos, 0, 0, 0));
}
uint16_t htons(uint16_t valor) { return (valor << 8) | (valor >> 8); }
uint16_t ntohs(uint16_t valor) { return htons(valor); }
uint32_t htonl(uint32_t valor) {
    return (valor << 24) | ((valor << 8) & 0xff0000U) | ((valor >> 8) & 0xff00U) | (valor >> 24);
}
uint32_t ntohl(uint32_t valor) { return htonl(valor); }
int inet_pton(int esquemaDirección, const char *Cadena, void *dirección) {
    if (esquemaDirección != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!Cadena || !dirección) { errno = EFAULT; return -1; }
    unsigned char valorTemporal[4];
    for (int entradaElementoRanura = 0; entradaElementoRanura < 4; entradaElementoRanura++) {
        int valor = 0, dígitos = 0;
        const char *ponerEnMarcha = Cadena;
        while (*Cadena >= '0' && *Cadena <= '9') {
            if (++dígitos > 3) return 0;
            valor = valor * 10 + *Cadena++ - '0';
        }
        if (!dígitos || valor > 255 || (dígitos > 1 && *ponerEnMarcha == '0')) return 0;
        valorTemporal[entradaElementoRanura] = valor;
        if (entradaElementoRanura < 3) { if (*Cadena++ != '.') return 0; }
        else if (*Cadena) return 0;
    }
    for (int entradaElementoRanura = 0; entradaElementoRanura < 4; entradaElementoRanura++) ((unsigned char *)dirección)[entradaElementoRanura] = valorTemporal[entradaElementoRanura];
    return 1;
}
const char *inet_ntop(int esquemaDirección, const void *dirección, char *Cadena, socklen_t valorCapacidad) {
    if (esquemaDirección != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!dirección || !Cadena) { errno = EFAULT; return 0; }
    const unsigned char *númeroValor = dirección;
    char valorTemporal[16]; unsigned int longitud = 0;
    for (int entradaElementoRanura = 0; entradaElementoRanura < 4; entradaElementoRanura++) {
        unsigned int valor = númeroValor[entradaElementoRanura];
        if (valor >= 100) valorTemporal[longitud++] = '0' + valor / 100;
        if (valor >= 10) valorTemporal[longitud++] = '0' + valor / 10 % 10;
        valorTemporal[longitud++] = '0' + valor % 10;
        if (entradaElementoRanura < 3) valorTemporal[longitud++] = '.';
    }
    valorTemporal[longitud++] = 0;
    if (valorCapacidad < longitud) { errno = ENOSPC; return 0; }
    for (unsigned int entradaElementoRanura = 0; entradaElementoRanura < longitud; entradaElementoRanura++) Cadena[entradaElementoRanura] = valorTemporal[entradaElementoRanura];
    return Cadena;
}
