#include <ağ_ABI.h>
#include <errno.h>
#include "Ara_sınır.h"

int socket(int 주소체계, int ağ_Tip, int 규약번호) {
    return çağrı_KR(jkoros_syscall(41, 주소체계, ağ_Tip, 규약번호, 0, 0));
}
int bind(int Dosya_tanımlayıcı, const struct sockaddr *ADRES, socklen_t ADRES_süre) {
    return çağrı_KR(jkoros_syscall(42, Dosya_tanımlayıcı, (int)ADRES, ADRES_süre, 0, 0));
}
ssize_t sendto(int Dosya_tanımlayıcı, const void *veri, size_t bayt_BAĞ_DEĞ_SAY, int Ayarlar,
               const struct sockaddr *ADRES, socklen_t ADRES_süre) {
    int istek[2] = {(int)ADRES, ADRES_süre};
    return çağrı_KR(jkoros_syscall(43, Dosya_tanımlayıcı, (int)veri, bayt_BAĞ_DEĞ_SAY, Ayarlar, (int)istek));
}
ssize_t recvfrom(int Dosya_tanımlayıcı, void *veri, size_t bayt_BAĞ_DEĞ_SAY, int Ayarlar,
                 struct sockaddr *ADRES, socklen_t *ADRES_süre) {
    int istek[2] = {(int)ADRES, (int)ADRES_süre};
    return çağrı_KR(jkoros_syscall(44, Dosya_tanımlayıcı, (int)veri, bayt_BAĞ_DEĞ_SAY, Ayarlar, (int)istek));
}
int getsockname(int Dosya_tanımlayıcı, struct sockaddr *ADRES, socklen_t *ADRES_süre) {
    return çağrı_KR(jkoros_syscall(45, Dosya_tanımlayıcı, (int)ADRES, (int)ADRES_süre, 0, 0));
}
int setsockopt(int Dosya_tanımlayıcı, int katman_değer_e65604ef, int Ayarlar_ad, const void *değer, socklen_t değer_süre) {
    if (katman_değer_e65604ef != SOL_SOCKET || Ayarlar_ad != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!değer) { errno = EFAULT; return -1; }
    if (değer_süre != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *zaman_değeri = değer;
    if (zaman_değeri->tv_sec < 0 || zaman_değeri->tv_sec > 2 || zaman_değeri->tv_usec < 0 || zaman_değeri->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = zaman_değeri->tv_sec * 1000 + (zaman_değeri->tv_usec + 999) / 1000;
    return çağrı_KR(jkoros_syscall(46, Dosya_tanımlayıcı, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t değer) { return (değer << 8) | (değer >> 8); }
uint16_t ntohs(uint16_t değer) { return htons(değer); }
uint32_t htonl(uint32_t değer) {
    return (değer << 24) | ((değer << 8) & 0xff0000U) | ((değer >> 8) & 0xff00U) | (değer >> 24);
}
uint32_t ntohl(uint32_t değer) { return htonl(değer); }
int inet_pton(int 주소체계, const char *dize_değer, void *ADRES) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!dize_değer || !ADRES) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int yuva_girdi = 0; yuva_girdi < 4; yuva_girdi++) {
        int değer = 0, 자릿수 = 0;
        const char *çalıştır = dize_değer;
        while (*dize_değer >= '0' && *dize_değer <= '9') {
            if (++자릿수 > 3) return 0;
            değer = değer * 10 + *dize_değer++ - '0';
        }
        if (!자릿수 || değer > 255 || (자릿수 > 1 && *çalıştır == '0')) return 0;
        임시[yuva_girdi] = değer;
        if (yuva_girdi < 3) { if (*dize_değer++ != '.') return 0; }
        else if (*dize_değer) return 0;
    }
    for (int yuva_girdi = 0; yuva_girdi < 4; yuva_girdi++) ((unsigned char *)ADRES)[yuva_girdi] = 임시[yuva_girdi];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ADRES, char *dize_değer, socklen_t kapasite_değer) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ADRES || !dize_değer) { errno = EFAULT; return 0; }
    const unsigned char *수 = ADRES;
    char 임시[16]; unsigned int süre_değer = 0;
    for (int yuva_girdi = 0; yuva_girdi < 4; yuva_girdi++) {
        unsigned int değer = 수[yuva_girdi];
        if (değer >= 100) 임시[süre_değer++] = '0' + değer / 100;
        if (değer >= 10) 임시[süre_değer++] = '0' + değer / 10 % 10;
        임시[süre_değer++] = '0' + değer % 10;
        if (yuva_girdi < 3) 임시[süre_değer++] = '.';
    }
    임시[süre_değer++] = 0;
    if (kapasite_değer < süre_değer) { errno = ENOSPC; return 0; }
    for (unsigned int yuva_girdi = 0; yuva_girdi < süre_değer; yuva_girdi++) dize_değer[yuva_girdi] = 임시[yuva_girdi];
    return dize_değer;
}
