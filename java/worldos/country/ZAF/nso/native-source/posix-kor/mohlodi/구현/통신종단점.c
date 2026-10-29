#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *atrese, socklen_t atrese_botelele) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)atrese, atrese_botelele, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t 바이트수, int Dipeakanyo,
               const struct sockaddr *atrese, socklen_t atrese_botelele) {
    int 요청[2] = {(int)atrese, atrese_botelele};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, 바이트수, Dipeakanyo, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t 바이트수, int Dipeakanyo,
                 struct sockaddr *atrese, socklen_t *atrese_botelele) {
    int 요청[2] = {(int)atrese, (int)atrese_botelele};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, 바이트수, Dipeakanyo, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *atrese, socklen_t *atrese_botelele) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)atrese, (int)atrese_botelele, 0, 0));
}
int setsockopt(int 파일서술자, int llaga_boleng, int Dipeakanyo_leina, const void *boleng, socklen_t boleng_botelele) {
    if (llaga_boleng != SOL_SOCKET || Dipeakanyo_leina != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!boleng) { errno = EFAULT; return -1; }
    if (boleng_botelele != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = boleng;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t boleng) { return (boleng << 8) | (boleng >> 8); }
uint16_t ntohs(uint16_t boleng) { return htons(boleng); }
uint32_t htonl(uint32_t boleng) {
    return (boleng << 24) | ((boleng << 8) & 0xff0000U) | ((boleng >> 8) & 0xff00U) | (boleng >> 24);
}
uint32_t ntohl(uint32_t boleng) { return htonl(boleng); }
int inet_pton(int 주소체계, const char *molokoloko_boleng, void *atrese) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!molokoloko_boleng || !atrese) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 4; sekgobana_go_tsenya_tshedimošo++) {
        int boleng = 0, 자릿수 = 0;
        const char *Diriša = molokoloko_boleng;
        while (*molokoloko_boleng >= '0' && *molokoloko_boleng <= '9') {
            if (++자릿수 > 3) return 0;
            boleng = boleng * 10 + *molokoloko_boleng++ - '0';
        }
        if (!자릿수 || boleng > 255 || (자릿수 > 1 && *Diriša == '0')) return 0;
        임시[sekgobana_go_tsenya_tshedimošo] = boleng;
        if (sekgobana_go_tsenya_tshedimošo < 3) { if (*molokoloko_boleng++ != '.') return 0; }
        else if (*molokoloko_boleng) return 0;
    }
    for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 4; sekgobana_go_tsenya_tshedimošo++) ((unsigned char *)atrese)[sekgobana_go_tsenya_tshedimošo] = 임시[sekgobana_go_tsenya_tshedimošo];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *atrese, char *molokoloko_boleng, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!atrese || !molokoloko_boleng) { errno = EFAULT; return 0; }
    const unsigned char *수 = atrese;
    char 임시[16]; unsigned int botelele_boleng = 0;
    for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 4; sekgobana_go_tsenya_tshedimošo++) {
        unsigned int boleng = 수[sekgobana_go_tsenya_tshedimošo];
        if (boleng >= 100) 임시[botelele_boleng++] = '0' + boleng / 100;
        if (boleng >= 10) 임시[botelele_boleng++] = '0' + boleng / 10 % 10;
        임시[botelele_boleng++] = '0' + boleng % 10;
        if (sekgobana_go_tsenya_tshedimošo < 3) 임시[botelele_boleng++] = '.';
    }
    임시[botelele_boleng++] = 0;
    if (용량 < botelele_boleng) { errno = ENOSPC; return 0; }
    for (unsigned int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < botelele_boleng; sekgobana_go_tsenya_tshedimošo++) molokoloko_boleng[sekgobana_go_tsenya_tshedimošo] = 임시[sekgobana_go_tsenya_tshedimošo];
    return molokoloko_boleng;
}
