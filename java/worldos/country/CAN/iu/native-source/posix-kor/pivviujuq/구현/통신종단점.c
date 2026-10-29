#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *turaarut, socklen_t turaarut_takininga) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)turaarut, turaarut_takininga, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *titiqqat, size_t 바이트수, int 설정,
               const struct sockaddr *turaarut, socklen_t turaarut_takininga) {
    int 요청[2] = {(int)turaarut, turaarut_takininga};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)titiqqat, 바이트수, 설정, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *titiqqat, size_t 바이트수, int 설정,
                 struct sockaddr *turaarut, socklen_t *turaarut_takininga) {
    int 요청[2] = {(int)turaarut, (int)turaarut_takininga};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)titiqqat, 바이트수, 설정, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *turaarut, socklen_t *turaarut_takininga) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)turaarut, (int)turaarut_takininga, 0, 0));
}
int setsockopt(int 파일서술자, int qaliriit_atuutilik, int 설정이름, const void *atuutilik, socklen_t atuutilik_takininga) {
    if (qaliriit_atuutilik != SOL_SOCKET || 설정이름 != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!atuutilik) { errno = EFAULT; return -1; }
    if (atuutilik_takininga != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = atuutilik;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t atuutilik) { return (atuutilik << 8) | (atuutilik >> 8); }
uint16_t ntohs(uint16_t atuutilik) { return htons(atuutilik); }
uint32_t htonl(uint32_t atuutilik) {
    return (atuutilik << 24) | ((atuutilik << 8) & 0xff0000U) | ((atuutilik >> 8) & 0xff00U) | (atuutilik >> 24);
}
uint32_t ntohl(uint32_t atuutilik) { return htonl(atuutilik); }
int inet_pton(int 주소체계, const char *qimiaq_atuutilik, void *turaarut) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!qimiaq_atuutilik || !turaarut) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int atuutilik = 0, 자릿수 = 0;
        const char *시작 = qimiaq_atuutilik;
        while (*qimiaq_atuutilik >= '0' && *qimiaq_atuutilik <= '9') {
            if (++자릿수 > 3) return 0;
            atuutilik = atuutilik * 10 + *qimiaq_atuutilik++ - '0';
        }
        if (!자릿수 || atuutilik > 255 || (자릿수 > 1 && *시작 == '0')) return 0;
        임시[칸] = atuutilik;
        if (칸 < 3) { if (*qimiaq_atuutilik++ != '.') return 0; }
        else if (*qimiaq_atuutilik) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)turaarut)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *turaarut, char *qimiaq_atuutilik, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!turaarut || !qimiaq_atuutilik) { errno = EFAULT; return 0; }
    const unsigned char *수 = turaarut;
    char 임시[16]; unsigned int takininga_atuutilik = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int atuutilik = 수[칸];
        if (atuutilik >= 100) 임시[takininga_atuutilik++] = '0' + atuutilik / 100;
        if (atuutilik >= 10) 임시[takininga_atuutilik++] = '0' + atuutilik / 10 % 10;
        임시[takininga_atuutilik++] = '0' + atuutilik % 10;
        if (칸 < 3) 임시[takininga_atuutilik++] = '.';
    }
    임시[takininga_atuutilik++] = 0;
    if (용량 < takininga_atuutilik) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < takininga_atuutilik; 칸++) qimiaq_atuutilik[칸] = 임시[칸];
    return qimiaq_atuutilik;
}
