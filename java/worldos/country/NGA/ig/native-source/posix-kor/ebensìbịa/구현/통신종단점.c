#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *àdreèsì, socklen_t àdreèsì_ogologo) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)àdreèsì, àdreèsì_ogologo, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *datà, size_t 바이트수, int Mwube,
               const struct sockaddr *àdreèsì, socklen_t àdreèsì_ogologo) {
    int 요청[2] = {(int)àdreèsì, àdreèsì_ogologo};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)datà, 바이트수, Mwube, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *datà, size_t 바이트수, int Mwube,
                 struct sockaddr *àdreèsì, socklen_t *àdreèsì_ogologo) {
    int 요청[2] = {(int)àdreèsì, (int)àdreèsì_ogologo};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)datà, 바이트수, Mwube, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *àdreèsì, socklen_t *àdreèsì_ogologo) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)àdreèsì, (int)àdreèsì_ogologo, 0, 0));
}
int setsockopt(int 파일서술자, int òkpùkpù_valuu, int Mwube_akara_ahà, const void *valuu, socklen_t valuu_ogologo) {
    if (òkpùkpù_valuu != SOL_SOCKET || Mwube_akara_ahà != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!valuu) { errno = EFAULT; return -1; }
    if (valuu_ogologo != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = valuu;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t valuu) { return (valuu << 8) | (valuu >> 8); }
uint16_t ntohs(uint16_t valuu) { return htons(valuu); }
uint32_t htonl(uint32_t valuu) {
    return (valuu << 24) | ((valuu << 8) & 0xff0000U) | ((valuu >> 8) & 0xff00U) | (valuu >> 24);
}
uint32_t ntohl(uint32_t valuu) { return htonl(valuu); }
int inet_pton(int 주소체계, const char *ùsòròokwū_valuu, void *àdreèsì) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ùsòròokwū_valuu || !àdreèsì) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int oghere_ndebà = 0; oghere_ndebà < 4; oghere_ndebà++) {
        int valuu = 0, 자릿수 = 0;
        const char *Bido = ùsòròokwū_valuu;
        while (*ùsòròokwū_valuu >= '0' && *ùsòròokwū_valuu <= '9') {
            if (++자릿수 > 3) return 0;
            valuu = valuu * 10 + *ùsòròokwū_valuu++ - '0';
        }
        if (!자릿수 || valuu > 255 || (자릿수 > 1 && *Bido == '0')) return 0;
        임시[oghere_ndebà] = valuu;
        if (oghere_ndebà < 3) { if (*ùsòròokwū_valuu++ != '.') return 0; }
        else if (*ùsòròokwū_valuu) return 0;
    }
    for (int oghere_ndebà = 0; oghere_ndebà < 4; oghere_ndebà++) ((unsigned char *)àdreèsì)[oghere_ndebà] = 임시[oghere_ndebà];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *àdreèsì, char *ùsòròokwū_valuu, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!àdreèsì || !ùsòròokwū_valuu) { errno = EFAULT; return 0; }
    const unsigned char *수 = àdreèsì;
    char 임시[16]; unsigned int ogologo_valuu = 0;
    for (int oghere_ndebà = 0; oghere_ndebà < 4; oghere_ndebà++) {
        unsigned int valuu = 수[oghere_ndebà];
        if (valuu >= 100) 임시[ogologo_valuu++] = '0' + valuu / 100;
        if (valuu >= 10) 임시[ogologo_valuu++] = '0' + valuu / 10 % 10;
        임시[ogologo_valuu++] = '0' + valuu % 10;
        if (oghere_ndebà < 3) 임시[ogologo_valuu++] = '.';
    }
    임시[ogologo_valuu++] = 0;
    if (용량 < ogologo_valuu) { errno = ENOSPC; return 0; }
    for (unsigned int oghere_ndebà = 0; oghere_ndebà < ogologo_valuu; oghere_ndebà++) ùsòròokwū_valuu[oghere_ndebà] = 임시[oghere_ndebà];
    return ùsòròokwū_valuu;
}
