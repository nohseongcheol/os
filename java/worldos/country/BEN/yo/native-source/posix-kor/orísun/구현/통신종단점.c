#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *àdírẹ́ẹ̀sì, socklen_t àdírẹ́ẹ̀sì_gígùn) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)àdírẹ́ẹ̀sì, àdírẹ́ẹ̀sì_gígùn, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *détà, size_t 바이트수, int Àwọn_ààtò,
               const struct sockaddr *àdírẹ́ẹ̀sì, socklen_t àdírẹ́ẹ̀sì_gígùn) {
    int 요청[2] = {(int)àdírẹ́ẹ̀sì, àdírẹ́ẹ̀sì_gígùn};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)détà, 바이트수, Àwọn_ààtò, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *détà, size_t 바이트수, int Àwọn_ààtò,
                 struct sockaddr *àdírẹ́ẹ̀sì, socklen_t *àdírẹ́ẹ̀sì_gígùn) {
    int 요청[2] = {(int)àdírẹ́ẹ̀sì, (int)àdírẹ́ẹ̀sì_gígùn};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)détà, 바이트수, Àwọn_ààtò, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *àdírẹ́ẹ̀sì, socklen_t *àdírẹ́ẹ̀sì_gígùn) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)àdírẹ́ẹ̀sì, (int)àdírẹ́ẹ̀sì_gígùn, 0, 0));
}
int setsockopt(int 파일서술자, int ìpele_iye, int Àwọn_ààtò_orúkọ, const void *iye, socklen_t iye_gígùn) {
    if (ìpele_iye != SOL_SOCKET || Àwọn_ààtò_orúkọ != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!iye) { errno = EFAULT; return -1; }
    if (iye_gígùn != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = iye;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t iye) { return (iye << 8) | (iye >> 8); }
uint16_t ntohs(uint16_t iye) { return htons(iye); }
uint32_t htonl(uint32_t iye) {
    return (iye << 24) | ((iye << 8) & 0xff0000U) | ((iye >> 8) & 0xff00U) | (iye >> 24);
}
uint32_t ntohl(uint32_t iye) { return htonl(iye); }
int inet_pton(int 주소체계, const char *fọ́nrán_iye, void *àdírẹ́ẹ̀sì) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!fọ́nrán_iye || !àdírẹ́ẹ̀sì) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 4; ààyè_ìfàyọkàsí_ìgbéwọlé++) {
        int iye = 0, 자릿수 = 0;
        const char *Rọ́ọ̀nù = fọ́nrán_iye;
        while (*fọ́nrán_iye >= '0' && *fọ́nrán_iye <= '9') {
            if (++자릿수 > 3) return 0;
            iye = iye * 10 + *fọ́nrán_iye++ - '0';
        }
        if (!자릿수 || iye > 255 || (자릿수 > 1 && *Rọ́ọ̀nù == '0')) return 0;
        임시[ààyè_ìfàyọkàsí_ìgbéwọlé] = iye;
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 3) { if (*fọ́nrán_iye++ != '.') return 0; }
        else if (*fọ́nrán_iye) return 0;
    }
    for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 4; ààyè_ìfàyọkàsí_ìgbéwọlé++) ((unsigned char *)àdírẹ́ẹ̀sì)[ààyè_ìfàyọkàsí_ìgbéwọlé] = 임시[ààyè_ìfàyọkàsí_ìgbéwọlé];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *àdírẹ́ẹ̀sì, char *fọ́nrán_iye, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!àdírẹ́ẹ̀sì || !fọ́nrán_iye) { errno = EFAULT; return 0; }
    const unsigned char *수 = àdírẹ́ẹ̀sì;
    char 임시[16]; unsigned int gígùn_iye = 0;
    for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 4; ààyè_ìfàyọkàsí_ìgbéwọlé++) {
        unsigned int iye = 수[ààyè_ìfàyọkàsí_ìgbéwọlé];
        if (iye >= 100) 임시[gígùn_iye++] = '0' + iye / 100;
        if (iye >= 10) 임시[gígùn_iye++] = '0' + iye / 10 % 10;
        임시[gígùn_iye++] = '0' + iye % 10;
        if (ààyè_ìfàyọkàsí_ìgbéwọlé < 3) 임시[gígùn_iye++] = '.';
    }
    임시[gígùn_iye++] = 0;
    if (용량 < gígùn_iye) { errno = ENOSPC; return 0; }
    for (unsigned int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < gígùn_iye; ààyè_ìfàyọkàsí_ìgbéwọlé++) fọ́nrán_iye[ààyè_ìfàyọkàsí_ìgbéwọlé] = 임시[ààyè_ìfàyọkàsí_ìgbéwọlé];
    return fọ́nrán_iye;
}
