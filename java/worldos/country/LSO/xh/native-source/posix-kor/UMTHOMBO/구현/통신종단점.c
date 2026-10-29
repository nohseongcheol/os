#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *idilesi, socklen_t idilesi_ubude) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)idilesi, idilesi_ubude, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *iingcombolo, size_t 바이트수, int Imimiselo,
               const struct sockaddr *idilesi, socklen_t idilesi_ubude) {
    int 요청[2] = {(int)idilesi, idilesi_ubude};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)iingcombolo, 바이트수, Imimiselo, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *iingcombolo, size_t 바이트수, int Imimiselo,
                 struct sockaddr *idilesi, socklen_t *idilesi_ubude) {
    int 요청[2] = {(int)idilesi, (int)idilesi_ubude};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)iingcombolo, 바이트수, Imimiselo, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *idilesi, socklen_t *idilesi_ubude) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)idilesi, (int)idilesi_ubude, 0, 0));
}
int setsockopt(int 파일서술자, int ileya_ixabiso, int Iisetingi_igama, const void *ixabiso, socklen_t ixabiso_ubude) {
    if (ileya_ixabiso != SOL_SOCKET || Iisetingi_igama != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ixabiso) { errno = EFAULT; return -1; }
    if (ixabiso_ubude != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = ixabiso;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ixabiso) { return (ixabiso << 8) | (ixabiso >> 8); }
uint16_t ntohs(uint16_t ixabiso) { return htons(ixabiso); }
uint32_t htonl(uint32_t ixabiso) {
    return (ixabiso << 24) | ((ixabiso << 8) & 0xff0000U) | ((ixabiso >> 8) & 0xff00U) | (ixabiso >> 24);
}
uint32_t ntohl(uint32_t ixabiso) { return htonl(ixabiso); }
int inet_pton(int 주소체계, const char *uluhlu_lweekharektha_ixabiso, void *idilesi) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!uluhlu_lweekharektha_ixabiso || !idilesi) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 4; isithuba_ufako_nkcukacha++) {
        int ixabiso = 0, 자릿수 = 0;
        const char *Phumeza = uluhlu_lweekharektha_ixabiso;
        while (*uluhlu_lweekharektha_ixabiso >= '0' && *uluhlu_lweekharektha_ixabiso <= '9') {
            if (++자릿수 > 3) return 0;
            ixabiso = ixabiso * 10 + *uluhlu_lweekharektha_ixabiso++ - '0';
        }
        if (!자릿수 || ixabiso > 255 || (자릿수 > 1 && *Phumeza == '0')) return 0;
        임시[isithuba_ufako_nkcukacha] = ixabiso;
        if (isithuba_ufako_nkcukacha < 3) { if (*uluhlu_lweekharektha_ixabiso++ != '.') return 0; }
        else if (*uluhlu_lweekharektha_ixabiso) return 0;
    }
    for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 4; isithuba_ufako_nkcukacha++) ((unsigned char *)idilesi)[isithuba_ufako_nkcukacha] = 임시[isithuba_ufako_nkcukacha];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *idilesi, char *uluhlu_lweekharektha_ixabiso, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!idilesi || !uluhlu_lweekharektha_ixabiso) { errno = EFAULT; return 0; }
    const unsigned char *수 = idilesi;
    char 임시[16]; unsigned int ubude_ixabiso = 0;
    for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 4; isithuba_ufako_nkcukacha++) {
        unsigned int ixabiso = 수[isithuba_ufako_nkcukacha];
        if (ixabiso >= 100) 임시[ubude_ixabiso++] = '0' + ixabiso / 100;
        if (ixabiso >= 10) 임시[ubude_ixabiso++] = '0' + ixabiso / 10 % 10;
        임시[ubude_ixabiso++] = '0' + ixabiso % 10;
        if (isithuba_ufako_nkcukacha < 3) 임시[ubude_ixabiso++] = '.';
    }
    임시[ubude_ixabiso++] = 0;
    if (용량 < ubude_ixabiso) { errno = ENOSPC; return 0; }
    for (unsigned int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < ubude_ixabiso; isithuba_ufako_nkcukacha++) uluhlu_lweekharektha_ixabiso[isithuba_ufako_nkcukacha] = 임시[isithuba_ufako_nkcukacha];
    return uluhlu_lweekharektha_ixabiso;
}
