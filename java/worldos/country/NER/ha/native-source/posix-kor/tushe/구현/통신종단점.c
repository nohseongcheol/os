#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *imel, socklen_t imel_Tsawo) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)imel, imel_Tsawo, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *Tarin_bayani, size_t 바이트수, int Saituna,
               const struct sockaddr *imel, socklen_t imel_Tsawo) {
    int 요청[2] = {(int)imel, imel_Tsawo};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)Tarin_bayani, 바이트수, Saituna, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *Tarin_bayani, size_t 바이트수, int Saituna,
                 struct sockaddr *imel, socklen_t *imel_Tsawo) {
    int 요청[2] = {(int)imel, (int)imel_Tsawo};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)Tarin_bayani, 바이트수, Saituna, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *imel, socklen_t *imel_Tsawo) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)imel, (int)imel_Tsawo, 0, 0));
}
int setsockopt(int 파일서술자, int Tsarkiya_Daraja, int Saituna_Suna, const void *Daraja, socklen_t Daraja_Tsawo) {
    if (Tsarkiya_Daraja != SOL_SOCKET || Saituna_Suna != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!Daraja) { errno = EFAULT; return -1; }
    if (Daraja_Tsawo != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *lokaci_Daraja = Daraja;
    if (lokaci_Daraja->tv_sec < 0 || lokaci_Daraja->tv_sec > 2 || lokaci_Daraja->tv_usec < 0 || lokaci_Daraja->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = lokaci_Daraja->tv_sec * 1000 + (lokaci_Daraja->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t Daraja) { return (Daraja << 8) | (Daraja >> 8); }
uint16_t ntohs(uint16_t Daraja) { return htons(Daraja); }
uint32_t htonl(uint32_t Daraja) {
    return (Daraja << 24) | ((Daraja << 8) & 0xff0000U) | ((Daraja >> 8) & 0xff00U) | (Daraja >> 24);
}
uint32_t ntohl(uint32_t Daraja) { return htonl(Daraja); }
int inet_pton(int 주소체계, const char *Zare_Daraja, void *imel) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!Zare_Daraja || !imel) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 4; rami_Mashigar_bayanai++) {
        int Daraja = 0, 자릿수 = 0;
        const char *Tafiyar_da = Zare_Daraja;
        while (*Zare_Daraja >= '0' && *Zare_Daraja <= '9') {
            if (++자릿수 > 3) return 0;
            Daraja = Daraja * 10 + *Zare_Daraja++ - '0';
        }
        if (!자릿수 || Daraja > 255 || (자릿수 > 1 && *Tafiyar_da == '0')) return 0;
        임시[rami_Mashigar_bayanai] = Daraja;
        if (rami_Mashigar_bayanai < 3) { if (*Zare_Daraja++ != '.') return 0; }
        else if (*Zare_Daraja) return 0;
    }
    for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 4; rami_Mashigar_bayanai++) ((unsigned char *)imel)[rami_Mashigar_bayanai] = 임시[rami_Mashigar_bayanai];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *imel, char *Zare_Daraja, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!imel || !Zare_Daraja) { errno = EFAULT; return 0; }
    const unsigned char *수 = imel;
    char 임시[16]; unsigned int Tsawo_Daraja = 0;
    for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 4; rami_Mashigar_bayanai++) {
        unsigned int Daraja = 수[rami_Mashigar_bayanai];
        if (Daraja >= 100) 임시[Tsawo_Daraja++] = '0' + Daraja / 100;
        if (Daraja >= 10) 임시[Tsawo_Daraja++] = '0' + Daraja / 10 % 10;
        임시[Tsawo_Daraja++] = '0' + Daraja % 10;
        if (rami_Mashigar_bayanai < 3) 임시[Tsawo_Daraja++] = '.';
    }
    임시[Tsawo_Daraja++] = 0;
    if (용량 < Tsawo_Daraja) { errno = ENOSPC; return 0; }
    for (unsigned int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < Tsawo_Daraja; rami_Mashigar_bayanai++) Zare_Daraja[rami_Mashigar_bayanai] = 임시[rami_Mashigar_bayanai];
    return Zare_Daraja;
}
