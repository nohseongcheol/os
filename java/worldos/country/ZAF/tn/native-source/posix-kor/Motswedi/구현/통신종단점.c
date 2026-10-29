#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *aterese, socklen_t aterese_boleele) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)aterese, aterese_boleele, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *tshedimosetso, size_t 바이트수, int Diseting,
               const struct sockaddr *aterese, socklen_t aterese_boleele) {
    int 요청[2] = {(int)aterese, aterese_boleele};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)tshedimosetso, 바이트수, Diseting, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *tshedimosetso, size_t 바이트수, int Diseting,
                 struct sockaddr *aterese, socklen_t *aterese_boleele) {
    int 요청[2] = {(int)aterese, (int)aterese_boleele};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)tshedimosetso, 바이트수, Diseting, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *aterese, socklen_t *aterese_boleele) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)aterese, (int)aterese_boleele, 0, 0));
}
int setsockopt(int 파일서술자, int boalo_Boleng, int Diseting_leina, const void *Boleng, socklen_t Boleng_boleele) {
    if (boalo_Boleng != SOL_SOCKET || Diseting_leina != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!Boleng) { errno = EFAULT; return -1; }
    if (Boleng_boleele != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = Boleng;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t Boleng) { return (Boleng << 8) | (Boleng >> 8); }
uint16_t ntohs(uint16_t Boleng) { return htons(Boleng); }
uint32_t htonl(uint32_t Boleng) {
    return (Boleng << 24) | ((Boleng << 8) & 0xff0000U) | ((Boleng >> 8) & 0xff00U) | (Boleng >> 24);
}
uint32_t ntohl(uint32_t Boleng) { return htonl(Boleng); }
int inet_pton(int 주소체계, const char *dikwalwa_Boleng, void *aterese) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!dikwalwa_Boleng || !aterese) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int sebaka_tsenyo = 0; sebaka_tsenyo < 4; sebaka_tsenyo++) {
        int Boleng = 0, 자릿수 = 0;
        const char *dirisa = dikwalwa_Boleng;
        while (*dikwalwa_Boleng >= '0' && *dikwalwa_Boleng <= '9') {
            if (++자릿수 > 3) return 0;
            Boleng = Boleng * 10 + *dikwalwa_Boleng++ - '0';
        }
        if (!자릿수 || Boleng > 255 || (자릿수 > 1 && *dirisa == '0')) return 0;
        임시[sebaka_tsenyo] = Boleng;
        if (sebaka_tsenyo < 3) { if (*dikwalwa_Boleng++ != '.') return 0; }
        else if (*dikwalwa_Boleng) return 0;
    }
    for (int sebaka_tsenyo = 0; sebaka_tsenyo < 4; sebaka_tsenyo++) ((unsigned char *)aterese)[sebaka_tsenyo] = 임시[sebaka_tsenyo];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *aterese, char *dikwalwa_Boleng, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!aterese || !dikwalwa_Boleng) { errno = EFAULT; return 0; }
    const unsigned char *수 = aterese;
    char 임시[16]; unsigned int boleele_Boleng = 0;
    for (int sebaka_tsenyo = 0; sebaka_tsenyo < 4; sebaka_tsenyo++) {
        unsigned int Boleng = 수[sebaka_tsenyo];
        if (Boleng >= 100) 임시[boleele_Boleng++] = '0' + Boleng / 100;
        if (Boleng >= 10) 임시[boleele_Boleng++] = '0' + Boleng / 10 % 10;
        임시[boleele_Boleng++] = '0' + Boleng % 10;
        if (sebaka_tsenyo < 3) 임시[boleele_Boleng++] = '.';
    }
    임시[boleele_Boleng++] = 0;
    if (용량 < boleele_Boleng) { errno = ENOSPC; return 0; }
    for (unsigned int sebaka_tsenyo = 0; sebaka_tsenyo < boleele_Boleng; sebaka_tsenyo++) dikwalwa_Boleng[sebaka_tsenyo] = 임시[sebaka_tsenyo];
    return dikwalwa_Boleng;
}
