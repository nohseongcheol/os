#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ADDRESS, socklen_t ADDRESS_roa) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ADDRESS, ADDRESS_roa, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *raraunga, size_t paita_COUNT, int Ngā_Tautuhinga,
               const struct sockaddr *ADDRESS, socklen_t ADDRESS_roa) {
    int 요청[2] = {(int)ADDRESS, ADDRESS_roa};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)raraunga, paita_COUNT, Ngā_Tautuhinga, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *raraunga, size_t paita_COUNT, int Ngā_Tautuhinga,
                 struct sockaddr *ADDRESS, socklen_t *ADDRESS_roa) {
    int 요청[2] = {(int)ADDRESS, (int)ADDRESS_roa};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)raraunga, paita_COUNT, Ngā_Tautuhinga, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ADDRESS, socklen_t *ADDRESS_roa) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ADDRESS, (int)ADDRESS_roa, 0, 0));
}
int setsockopt(int 파일서술자, int apa_uara, int Ngā_Tautuhinga_ingoa, const void *uara, socklen_t uara_roa) {
    if (apa_uara != SOL_SOCKET || Ngā_Tautuhinga_ingoa != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!uara) { errno = EFAULT; return -1; }
    if (uara_roa != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *TIME_uara = uara;
    if (TIME_uara->tv_sec < 0 || TIME_uara->tv_sec > 2 || TIME_uara->tv_usec < 0 || TIME_uara->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = TIME_uara->tv_sec * 1000 + (TIME_uara->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t uara) { return (uara << 8) | (uara >> 8); }
uint16_t ntohs(uint16_t uara) { return htons(uara); }
uint32_t htonl(uint32_t uara) {
    return (uara << 24) | ((uara << 8) & 0xff0000U) | ((uara >> 8) & 0xff00U) | (uara >> 24);
}
uint32_t ntohl(uint32_t uara) { return htonl(uara); }
int inet_pton(int 주소체계, const char *aho_uara, void *ADDRESS) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!aho_uara || !ADDRESS) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 4; kāniwha_tāurunga++) {
        int uara = 0, 자릿수 = 0;
        const char *whakahaere = aho_uara;
        while (*aho_uara >= '0' && *aho_uara <= '9') {
            if (++자릿수 > 3) return 0;
            uara = uara * 10 + *aho_uara++ - '0';
        }
        if (!자릿수 || uara > 255 || (자릿수 > 1 && *whakahaere == '0')) return 0;
        임시[kāniwha_tāurunga] = uara;
        if (kāniwha_tāurunga < 3) { if (*aho_uara++ != '.') return 0; }
        else if (*aho_uara) return 0;
    }
    for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 4; kāniwha_tāurunga++) ((unsigned char *)ADDRESS)[kāniwha_tāurunga] = 임시[kāniwha_tāurunga];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ADDRESS, char *aho_uara, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ADDRESS || !aho_uara) { errno = EFAULT; return 0; }
    const unsigned char *수 = ADDRESS;
    char 임시[16]; unsigned int roa_uara = 0;
    for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 4; kāniwha_tāurunga++) {
        unsigned int uara = 수[kāniwha_tāurunga];
        if (uara >= 100) 임시[roa_uara++] = '0' + uara / 100;
        if (uara >= 10) 임시[roa_uara++] = '0' + uara / 10 % 10;
        임시[roa_uara++] = '0' + uara % 10;
        if (kāniwha_tāurunga < 3) 임시[roa_uara++] = '.';
    }
    임시[roa_uara++] = 0;
    if (용량 < roa_uara) { errno = ENOSPC; return 0; }
    for (unsigned int kāniwha_tāurunga = 0; kāniwha_tāurunga < roa_uara; kāniwha_tāurunga++) aho_uara[kāniwha_tāurunga] = 임시[kāniwha_tāurunga];
    return aho_uara;
}
