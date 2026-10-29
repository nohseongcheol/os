#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ñiiɓirde, socklen_t ñiiɓirde_njuuteendi) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ñiiɓirde, ñiiɓirde_njuuteendi, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *keɓe, size_t 바이트수, int 설정,
               const struct sockaddr *ñiiɓirde, socklen_t ñiiɓirde_njuuteendi) {
    int 요청[2] = {(int)ñiiɓirde, ñiiɓirde_njuuteendi};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)keɓe, 바이트수, 설정, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *keɓe, size_t 바이트수, int 설정,
                 struct sockaddr *ñiiɓirde, socklen_t *ñiiɓirde_njuuteendi) {
    int 요청[2] = {(int)ñiiɓirde, (int)ñiiɓirde_njuuteendi};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)keɓe, 바이트수, 설정, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ñiiɓirde, socklen_t *ñiiɓirde_njuuteendi) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ñiiɓirde, (int)ñiiɓirde_njuuteendi, 0, 0));
}
int setsockopt(int 파일서술자, int tekkeendi_njaru, int 설정이름, const void *njaru, socklen_t njaru_njuuteendi) {
    if (tekkeendi_njaru != SOL_SOCKET || 설정이름 != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!njaru) { errno = EFAULT; return -1; }
    if (njaru_njuuteendi != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = njaru;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t njaru) { return (njaru << 8) | (njaru >> 8); }
uint16_t ntohs(uint16_t njaru) { return htons(njaru); }
uint32_t htonl(uint32_t njaru) {
    return (njaru << 24) | ((njaru << 8) & 0xff0000U) | ((njaru >> 8) & 0xff00U) | (njaru >> 24);
}
uint32_t ntohl(uint32_t njaru) { return htonl(njaru); }
int inet_pton(int 주소체계, const char *ɓoggol_njaru, void *ñiiɓirde) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ɓoggol_njaru || !ñiiɓirde) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int njaru = 0, 자릿수 = 0;
        const char *huutoraade = ɓoggol_njaru;
        while (*ɓoggol_njaru >= '0' && *ɓoggol_njaru <= '9') {
            if (++자릿수 > 3) return 0;
            njaru = njaru * 10 + *ɓoggol_njaru++ - '0';
        }
        if (!자릿수 || njaru > 255 || (자릿수 > 1 && *huutoraade == '0')) return 0;
        임시[칸] = njaru;
        if (칸 < 3) { if (*ɓoggol_njaru++ != '.') return 0; }
        else if (*ɓoggol_njaru) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)ñiiɓirde)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ñiiɓirde, char *ɓoggol_njaru, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ñiiɓirde || !ɓoggol_njaru) { errno = EFAULT; return 0; }
    const unsigned char *수 = ñiiɓirde;
    char 임시[16]; unsigned int njuuteendi_njaru = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int njaru = 수[칸];
        if (njaru >= 100) 임시[njuuteendi_njaru++] = '0' + njaru / 100;
        if (njaru >= 10) 임시[njuuteendi_njaru++] = '0' + njaru / 10 % 10;
        임시[njuuteendi_njaru++] = '0' + njaru % 10;
        if (칸 < 3) 임시[njuuteendi_njaru++] = '.';
    }
    임시[njuuteendi_njaru++] = 0;
    if (용량 < njuuteendi_njaru) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < njuuteendi_njaru; 칸++) ɓoggol_njaru[칸] = 임시[칸];
    return ɓoggol_njaru;
}
