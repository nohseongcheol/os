#include <сеть_ABI.h>
#include <errno.h>
#include "вызов_граница.h"

int socket(int 주소체계, int сеть_Вид, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, сеть_Вид, 규약번호, 0, 0));
}
int bind(int файл_дескриптор, const struct sockaddr *АДРЕС, socklen_t АДРЕС_длина) {
    return 호출결과(jkoros_syscall(42, файл_дескриптор, (int)АДРЕС, АДРЕС_длина, 0, 0));
}
ssize_t sendto(int файл_дескриптор, const void *данные, size_t байт_СЧЁТ, int Настройки,
               const struct sockaddr *АДРЕС, socklen_t АДРЕС_длина) {
    int запрос[2] = {(int)АДРЕС, АДРЕС_длина};
    return 호출결과(jkoros_syscall(43, файл_дескриптор, (int)данные, байт_СЧЁТ, Настройки, (int)запрос));
}
ssize_t recvfrom(int файл_дескриптор, void *данные, size_t байт_СЧЁТ, int Настройки,
                 struct sockaddr *АДРЕС, socklen_t *АДРЕС_длина) {
    int запрос[2] = {(int)АДРЕС, (int)АДРЕС_длина};
    return 호출결과(jkoros_syscall(44, файл_дескриптор, (int)данные, байт_СЧЁТ, Настройки, (int)запрос));
}
int getsockname(int файл_дескриптор, struct sockaddr *АДРЕС, socklen_t *АДРЕС_длина) {
    return 호출결과(jkoros_syscall(45, файл_дескриптор, (int)АДРЕС, (int)АДРЕС_длина, 0, 0));
}
int setsockopt(int файл_дескриптор, int слой_ЗНАЧЕН, int Настройки_имя, const void *ЗНАЧЕН, socklen_t ЗНАЧЕН_длина) {
    if (слой_ЗНАЧЕН != SOL_SOCKET || Настройки_имя != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ЗНАЧЕН) { errno = EFAULT; return -1; }
    if (ЗНАЧЕН_длина != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *значение_времени = ЗНАЧЕН;
    if (значение_времени->tv_sec < 0 || значение_времени->tv_sec > 2 || значение_времени->tv_usec < 0 || значение_времени->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = значение_времени->tv_sec * 1000 + (значение_времени->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, файл_дескриптор, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ЗНАЧЕН) { return (ЗНАЧЕН << 8) | (ЗНАЧЕН >> 8); }
uint16_t ntohs(uint16_t ЗНАЧЕН) { return htons(ЗНАЧЕН); }
uint32_t htonl(uint32_t ЗНАЧЕН) {
    return (ЗНАЧЕН << 24) | ((ЗНАЧЕН << 8) & 0xff0000U) | ((ЗНАЧЕН >> 8) & 0xff00U) | (ЗНАЧЕН >> 24);
}
uint32_t ntohl(uint32_t ЗНАЧЕН) { return htonl(ЗНАЧЕН); }
int inet_pton(int 주소체계, const char *строка_ЗНАЧЕН, void *АДРЕС) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!строка_ЗНАЧЕН || !АДРЕС) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int слот_ввод = 0; слот_ввод < 4; слот_ввод++) {
        int ЗНАЧЕН = 0, 자릿수 = 0;
        const char *запустить = строка_ЗНАЧЕН;
        while (*строка_ЗНАЧЕН >= '0' && *строка_ЗНАЧЕН <= '9') {
            if (++자릿수 > 3) return 0;
            ЗНАЧЕН = ЗНАЧЕН * 10 + *строка_ЗНАЧЕН++ - '0';
        }
        if (!자릿수 || ЗНАЧЕН > 255 || (자릿수 > 1 && *запустить == '0')) return 0;
        임시[слот_ввод] = ЗНАЧЕН;
        if (слот_ввод < 3) { if (*строка_ЗНАЧЕН++ != '.') return 0; }
        else if (*строка_ЗНАЧЕН) return 0;
    }
    for (int слот_ввод = 0; слот_ввод < 4; слот_ввод++) ((unsigned char *)АДРЕС)[слот_ввод] = 임시[слот_ввод];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *АДРЕС, char *строка_ЗНАЧЕН, socklen_t емкость_ЗНАЧЕН) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!АДРЕС || !строка_ЗНАЧЕН) { errno = EFAULT; return 0; }
    const unsigned char *수 = АДРЕС;
    char 임시[16]; unsigned int длина_ЗНАЧЕН = 0;
    for (int слот_ввод = 0; слот_ввод < 4; слот_ввод++) {
        unsigned int ЗНАЧЕН = 수[слот_ввод];
        if (ЗНАЧЕН >= 100) 임시[длина_ЗНАЧЕН++] = '0' + ЗНАЧЕН / 100;
        if (ЗНАЧЕН >= 10) 임시[длина_ЗНАЧЕН++] = '0' + ЗНАЧЕН / 10 % 10;
        임시[длина_ЗНАЧЕН++] = '0' + ЗНАЧЕН % 10;
        if (слот_ввод < 3) 임시[длина_ЗНАЧЕН++] = '.';
    }
    임시[длина_ЗНАЧЕН++] = 0;
    if (емкость_ЗНАЧЕН < длина_ЗНАЧЕН) { errno = ENOSPC; return 0; }
    for (unsigned int слот_ввод = 0; слот_ввод < длина_ЗНАЧЕН; слот_ввод++) строка_ЗНАЧЕН[слот_ввод] = 임시[слот_ввод];
    return строка_ЗНАЧЕН;
}
