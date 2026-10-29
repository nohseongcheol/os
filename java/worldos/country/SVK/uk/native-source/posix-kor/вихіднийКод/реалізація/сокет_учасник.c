#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *Адреса, socklen_t 주소길이) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)Адреса, 주소길이, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *дані, size_t 바이트수, int Налаштування,
               const struct sockaddr *Адреса, socklen_t 주소길이) {
    int запит[2] = {(int)Адреса, 주소길이};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)дані, 바이트수, Налаштування, (int)запит));
}
ssize_t recvfrom(int 파일서술자, void *дані, size_t 바이트수, int Налаштування,
                 struct sockaddr *Адреса, socklen_t *주소길이) {
    int запит[2] = {(int)Адреса, (int)주소길이};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)дані, 바이트수, Налаштування, (int)запит));
}
int getsockname(int 파일서술자, struct sockaddr *Адреса, socklen_t *주소길이) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)Адреса, (int)주소길이, 0, 0));
}
int setsockopt(int 파일서술자, int шар_значення, int Настройки_ім_я, const void *значення, socklen_t 값길이) {
    if (шар_значення != SOL_SOCKET || Настройки_ім_я != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!значення) { errno = EFAULT; return -1; }
    if (값길이 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *час_значення = значення;
    if (час_значення->tv_sec < 0 || час_значення->tv_sec > 2 || час_значення->tv_usec < 0 || час_значення->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = час_значення->tv_sec * 1000 + (час_значення->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t значення) { return (значення << 8) | (значення >> 8); }
uint16_t ntohs(uint16_t значення) { return htons(значення); }
uint32_t htonl(uint32_t значення) {
    return (значення << 24) | ((значення << 8) & 0xff0000U) | ((значення >> 8) & 0xff00U) | (значення >> 24);
}
uint32_t ntohl(uint32_t значення) { return htonl(значення); }
int inet_pton(int 주소체계, const char *рядок_значення, void *Адреса) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!рядок_значення || !Адреса) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int значення = 0, 자릿수 = 0;
        const char *запустити = рядок_значення;
        while (*рядок_значення >= '0' && *рядок_значення <= '9') {
            if (++자릿수 > 3) return 0;
            значення = значення * 10 + *рядок_значення++ - '0';
        }
        if (!자릿수 || значення > 255 || (자릿수 > 1 && *запустити == '0')) return 0;
        임시[칸] = значення;
        if (칸 < 3) { if (*рядок_значення++ != '.') return 0; }
        else if (*рядок_значення) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)Адреса)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *Адреса, char *рядок_значення, socklen_t ресурс_значення_e6ac1362) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!Адреса || !рядок_значення) { errno = EFAULT; return 0; }
    const unsigned char *수 = Адреса;
    char 임시[16]; unsigned int 길이 = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int значення = 수[칸];
        if (значення >= 100) 임시[길이++] = '0' + значення / 100;
        if (значення >= 10) 임시[길이++] = '0' + значення / 10 % 10;
        임시[길이++] = '0' + значення % 10;
        if (칸 < 3) 임시[길이++] = '.';
    }
    임시[길이++] = 0;
    if (ресурс_значення_e6ac1362 < 길이) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < 길이; 칸++) рядок_значення[칸] = 임시[칸];
    return рядок_значення;
}
