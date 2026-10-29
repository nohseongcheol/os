#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *helbide, socklen_t helbide_luzera) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)helbide, helbide_luzera, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *datuak, size_t byte_ZENBATU, int Ezarpenak,
               const struct sockaddr *helbide, socklen_t helbide_luzera) {
    int eskaera[2] = {(int)helbide, helbide_luzera};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)datuak, byte_ZENBATU, Ezarpenak, (int)eskaera));
}
ssize_t recvfrom(int 파일서술자, void *datuak, size_t byte_ZENBATU, int Ezarpenak,
                 struct sockaddr *helbide, socklen_t *helbide_luzera) {
    int eskaera[2] = {(int)helbide, (int)helbide_luzera};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)datuak, byte_ZENBATU, Ezarpenak, (int)eskaera));
}
int getsockname(int 파일서술자, struct sockaddr *helbide, socklen_t *helbide_luzera) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)helbide, (int)helbide_luzera, 0, 0));
}
int setsockopt(int 파일서술자, int maila_balio, int Ezarpenak_izen, const void *balio, socklen_t balio_luzera) {
    if (maila_balio != SOL_SOCKET || Ezarpenak_izen != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!balio) { errno = EFAULT; return -1; }
    if (balio_luzera != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *ordua_balio = balio;
    if (ordua_balio->tv_sec < 0 || ordua_balio->tv_sec > 2 || ordua_balio->tv_usec < 0 || ordua_balio->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = ordua_balio->tv_sec * 1000 + (ordua_balio->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t balio) { return (balio << 8) | (balio >> 8); }
uint16_t ntohs(uint16_t balio) { return htons(balio); }
uint32_t htonl(uint32_t balio) {
    return (balio << 24) | ((balio << 8) & 0xff0000U) | ((balio >> 8) & 0xff00U) | (balio >> 24);
}
uint32_t ntohl(uint32_t balio) { return htonl(balio); }
int inet_pton(int 주소체계, const char *kate_balio, void *helbide) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!kate_balio || !helbide) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int balio = 0, 자릿수 = 0;
        const char *Exekutatu_2 = kate_balio;
        while (*kate_balio >= '0' && *kate_balio <= '9') {
            if (++자릿수 > 3) return 0;
            balio = balio * 10 + *kate_balio++ - '0';
        }
        if (!자릿수 || balio > 255 || (자릿수 > 1 && *Exekutatu_2 == '0')) return 0;
        임시[칸] = balio;
        if (칸 < 3) { if (*kate_balio++ != '.') return 0; }
        else if (*kate_balio) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)helbide)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *helbide, char *kate_balio, socklen_t ahalmen_balio) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!helbide || !kate_balio) { errno = EFAULT; return 0; }
    const unsigned char *수 = helbide;
    char 임시[16]; unsigned int luzera_balio = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int balio = 수[칸];
        if (balio >= 100) 임시[luzera_balio++] = '0' + balio / 100;
        if (balio >= 10) 임시[luzera_balio++] = '0' + balio / 10 % 10;
        임시[luzera_balio++] = '0' + balio % 10;
        if (칸 < 3) 임시[luzera_balio++] = '.';
    }
    임시[luzera_balio++] = 0;
    if (ahalmen_balio < luzera_balio) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < luzera_balio; 칸++) kate_balio[칸] = 임시[칸];
    return kate_balio;
}
