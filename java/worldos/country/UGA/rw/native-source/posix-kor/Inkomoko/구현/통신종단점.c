#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *aderesi, socklen_t aderesi_uburebure) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)aderesi, aderesi_uburebure, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *amakurushingiro, size_t 바이트수, int Amagenamiterere,
               const struct sockaddr *aderesi, socklen_t aderesi_uburebure) {
    int 요청[2] = {(int)aderesi, aderesi_uburebure};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)amakurushingiro, 바이트수, Amagenamiterere, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *amakurushingiro, size_t 바이트수, int Amagenamiterere,
                 struct sockaddr *aderesi, socklen_t *aderesi_uburebure) {
    int 요청[2] = {(int)aderesi, (int)aderesi_uburebure};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)amakurushingiro, 바이트수, Amagenamiterere, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *aderesi, socklen_t *aderesi_uburebure) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)aderesi, (int)aderesi_uburebure, 0, 0));
}
int setsockopt(int 파일서술자, int akugara_agaciro, int Amagenamiterere_izina, const void *agaciro, socklen_t agaciro_uburebure) {
    if (akugara_agaciro != SOL_SOCKET || Amagenamiterere_izina != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!agaciro) { errno = EFAULT; return -1; }
    if (agaciro_uburebure != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = agaciro;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t agaciro) { return (agaciro << 8) | (agaciro >> 8); }
uint16_t ntohs(uint16_t agaciro) { return htons(agaciro); }
uint32_t htonl(uint32_t agaciro) {
    return (agaciro << 24) | ((agaciro << 8) & 0xff0000U) | ((agaciro >> 8) & 0xff00U) | (agaciro >> 24);
}
uint32_t ntohl(uint32_t agaciro) { return htonl(agaciro); }
int inet_pton(int 주소체계, const char *igicenteruro_agaciro, void *aderesi) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!igicenteruro_agaciro || !aderesi) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 4; umwanya_icyinjizwa++) {
        int agaciro = 0, 자릿수 = 0;
        const char *ihuriro = igicenteruro_agaciro;
        while (*igicenteruro_agaciro >= '0' && *igicenteruro_agaciro <= '9') {
            if (++자릿수 > 3) return 0;
            agaciro = agaciro * 10 + *igicenteruro_agaciro++ - '0';
        }
        if (!자릿수 || agaciro > 255 || (자릿수 > 1 && *ihuriro == '0')) return 0;
        임시[umwanya_icyinjizwa] = agaciro;
        if (umwanya_icyinjizwa < 3) { if (*igicenteruro_agaciro++ != '.') return 0; }
        else if (*igicenteruro_agaciro) return 0;
    }
    for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 4; umwanya_icyinjizwa++) ((unsigned char *)aderesi)[umwanya_icyinjizwa] = 임시[umwanya_icyinjizwa];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *aderesi, char *igicenteruro_agaciro, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!aderesi || !igicenteruro_agaciro) { errno = EFAULT; return 0; }
    const unsigned char *수 = aderesi;
    char 임시[16]; unsigned int uburebure_agaciro = 0;
    for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 4; umwanya_icyinjizwa++) {
        unsigned int agaciro = 수[umwanya_icyinjizwa];
        if (agaciro >= 100) 임시[uburebure_agaciro++] = '0' + agaciro / 100;
        if (agaciro >= 10) 임시[uburebure_agaciro++] = '0' + agaciro / 10 % 10;
        임시[uburebure_agaciro++] = '0' + agaciro % 10;
        if (umwanya_icyinjizwa < 3) 임시[uburebure_agaciro++] = '.';
    }
    임시[uburebure_agaciro++] = 0;
    if (용량 < uburebure_agaciro) { errno = ENOSPC; return 0; }
    for (unsigned int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < uburebure_agaciro; umwanya_icyinjizwa++) igicenteruro_agaciro[umwanya_icyinjizwa] = 임시[umwanya_icyinjizwa];
    return igicenteruro_agaciro;
}
