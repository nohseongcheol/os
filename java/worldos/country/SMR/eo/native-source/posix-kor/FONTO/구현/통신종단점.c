#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *주소, socklen_t 주소길이) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)주소, 주소길이, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *자료, size_t 바이트수, int Agordoj,
               const struct sockaddr *주소, socklen_t 주소길이) {
    int 요청[2] = {(int)주소, 주소길이};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)자료, 바이트수, Agordoj, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *자료, size_t 바이트수, int Agordoj,
                 struct sockaddr *주소, socklen_t *주소길이) {
    int 요청[2] = {(int)주소, (int)주소길이};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)자료, 바이트수, Agordoj, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *주소, socklen_t *주소길이) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)주소, (int)주소길이, 0, 0));
}
int setsockopt(int 파일서술자, int 계층, int 설정이름, const void *값, socklen_t 값길이) {
    if (계층 != SOL_SOCKET || 설정이름 != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!값) { errno = EFAULT; return -1; }
    if (값길이 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = 값;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t 값) { return (값 << 8) | (값 >> 8); }
uint16_t ntohs(uint16_t 값) { return htons(값); }
uint32_t htonl(uint32_t 값) {
    return (값 << 24) | ((값 << 8) & 0xff0000U) | ((값 >> 8) & 0xff00U) | (값 >> 24);
}
uint32_t ntohl(uint32_t 값) { return htonl(값); }
int inet_pton(int 주소체계, const char *문자열, void *주소) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!문자열 || !주소) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int 값 = 0, 자릿수 = 0;
        const char *Ruli = 문자열;
        while (*문자열 >= '0' && *문자열 <= '9') {
            if (++자릿수 > 3) return 0;
            값 = 값 * 10 + *문자열++ - '0';
        }
        if (!자릿수 || 값 > 255 || (자릿수 > 1 && *Ruli == '0')) return 0;
        임시[칸] = 값;
        if (칸 < 3) { if (*문자열++ != '.') return 0; }
        else if (*문자열) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)주소)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *주소, char *문자열, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!주소 || !문자열) { errno = EFAULT; return 0; }
    const unsigned char *수 = 주소;
    char 임시[16]; unsigned int 길이 = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int 값 = 수[칸];
        if (값 >= 100) 임시[길이++] = '0' + 값 / 100;
        if (값 >= 10) 임시[길이++] = '0' + 값 / 10 % 10;
        임시[길이++] = '0' + 값 % 10;
        if (칸 < 3) 임시[길이++] = '.';
    }
    임시[길이++] = 0;
    if (용량 < 길이) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < 길이; 칸++) 문자열[칸] = 임시[칸];
    return 문자열;
}
