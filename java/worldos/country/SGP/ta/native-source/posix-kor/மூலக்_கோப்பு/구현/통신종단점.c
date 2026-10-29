#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *முகவரி, socklen_t முகவரி_நீளம்) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)முகவரி, முகவரி_நீளம், 0, 0));
}
ssize_t sendto(int 파일서술자, const void *தரவு, size_t 바이트수, int அமைப்புகள்,
               const struct sockaddr *முகவரி, socklen_t முகவரி_நீளம்) {
    int HTTP_வேண்டுதல்[2] = {(int)முகவரி, முகவரி_நீளம்};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)தரவு, 바이트수, அமைப்புகள், (int)HTTP_வேண்டுதல்));
}
ssize_t recvfrom(int 파일서술자, void *தரவு, size_t 바이트수, int அமைப்புகள்,
                 struct sockaddr *முகவரி, socklen_t *முகவரி_நீளம்) {
    int HTTP_வேண்டுதல்[2] = {(int)முகவரி, (int)முகவரி_நீளம்};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)தரவு, 바이트수, அமைப்புகள், (int)HTTP_வேண்டுதல்));
}
int getsockname(int 파일서술자, struct sockaddr *முகவரி, socklen_t *முகவரி_நீளம்) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)முகவரி, (int)முகவரி_நீளம், 0, 0));
}
int setsockopt(int 파일서술자, int அடுக்கு_மதிப்பு, int அமைப்புகள்_பெயர், const void *மதிப்பு, socklen_t மதிப்பு_நீளம்) {
    if (அடுக்கு_மதிப்பு != SOL_SOCKET || அமைப்புகள்_பெயர் != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!மதிப்பு) { errno = EFAULT; return -1; }
    if (மதிப்பு_நீளம் != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *நேர_மதிப்பு = மதிப்பு;
    if (நேர_மதிப்பு->tv_sec < 0 || நேர_மதிப்பு->tv_sec > 2 || நேர_மதிப்பு->tv_usec < 0 || நேர_மதிப்பு->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = நேர_மதிப்பு->tv_sec * 1000 + (நேர_மதிப்பு->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t மதிப்பு) { return (மதிப்பு << 8) | (மதிப்பு >> 8); }
uint16_t ntohs(uint16_t மதிப்பு) { return htons(மதிப்பு); }
uint32_t htonl(uint32_t மதிப்பு) {
    return (மதிப்பு << 24) | ((மதிப்பு << 8) & 0xff0000U) | ((மதிப்பு >> 8) & 0xff00U) | (மதிப்பு >> 24);
}
uint32_t ntohl(uint32_t மதிப்பு) { return htonl(மதிப்பு); }
int inet_pton(int 주소체계, const char *சரம்_மதிப்பு, void *முகவரி) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!சரம்_மதிப்பு || !முகவரி) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int ஸ்லாட்_உள்ளீடு = 0; ஸ்லாட்_உள்ளீடு < 4; ஸ்லாட்_உள்ளீடு++) {
        int மதிப்பு = 0, 자릿수 = 0;
        const char *செயல்படுத்துக = சரம்_மதிப்பு;
        while (*சரம்_மதிப்பு >= '0' && *சரம்_மதிப்பு <= '9') {
            if (++자릿수 > 3) return 0;
            மதிப்பு = மதிப்பு * 10 + *சரம்_மதிப்பு++ - '0';
        }
        if (!자릿수 || மதிப்பு > 255 || (자릿수 > 1 && *செயல்படுத்துக == '0')) return 0;
        임시[ஸ்லாட்_உள்ளீடு] = மதிப்பு;
        if (ஸ்லாட்_உள்ளீடு < 3) { if (*சரம்_மதிப்பு++ != '.') return 0; }
        else if (*சரம்_மதிப்பு) return 0;
    }
    for (int ஸ்லாட்_உள்ளீடு = 0; ஸ்லாட்_உள்ளீடு < 4; ஸ்லாட்_உள்ளீடு++) ((unsigned char *)முகவரி)[ஸ்லாட்_உள்ளீடு] = 임시[ஸ்லாட்_உள்ளீடு];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *முகவரி, char *சரம்_மதிப்பு, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!முகவரி || !சரம்_மதிப்பு) { errno = EFAULT; return 0; }
    const unsigned char *수 = முகவரி;
    char 임시[16]; unsigned int நீளம்_மதிப்பு = 0;
    for (int ஸ்லாட்_உள்ளீடு = 0; ஸ்லாட்_உள்ளீடு < 4; ஸ்லாட்_உள்ளீடு++) {
        unsigned int மதிப்பு = 수[ஸ்லாட்_உள்ளீடு];
        if (மதிப்பு >= 100) 임시[நீளம்_மதிப்பு++] = '0' + மதிப்பு / 100;
        if (மதிப்பு >= 10) 임시[நீளம்_மதிப்பு++] = '0' + மதிப்பு / 10 % 10;
        임시[நீளம்_மதிப்பு++] = '0' + மதிப்பு % 10;
        if (ஸ்லாட்_உள்ளீடு < 3) 임시[நீளம்_மதிப்பு++] = '.';
    }
    임시[நீளம்_மதிப்பு++] = 0;
    if (용량 < நீளம்_மதிப்பு) { errno = ENOSPC; return 0; }
    for (unsigned int ஸ்லாட்_உள்ளீடு = 0; ஸ்லாட்_உள்ளீடு < நீளம்_மதிப்பு; ஸ்லாட்_உள்ளீடு++) சரம்_மதிப்பு[ஸ்லாட்_உள்ளீடு] = 임시[ஸ்லாட்_உள்ளீடு];
    return சரம்_மதிப்பு;
}
