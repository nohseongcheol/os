#include <ABIMạng.h>
#include <errno.h>
#include "RanhGiớiGọi.h"

int socket(int lượcĐồĐịaChỉ, int loạiMạng, int sốQuyƯớc) {
    return kếtQuảLờiGọi(jkoros_syscall(41, lượcĐồĐịaChỉ, loạiMạng, sốQuyƯớc, 0, 0));
}
int bind(int bộMôTảTệp, const struct sockaddr *địaChỉ, socklen_t độDàiĐịaChỉ) {
    return kếtQuảLờiGọi(jkoros_syscall(42, bộMôTảTệp, (int)địaChỉ, độDàiĐịaChỉ, 0, 0));
}
ssize_t sendto(int bộMôTảTệp, const void *DữLiệu, size_t sốLượngByte, int cácThiếtLập,
               const struct sockaddr *địaChỉ, socklen_t độDàiĐịaChỉ) {
    int yêuCầu[2] = {(int)địaChỉ, độDàiĐịaChỉ};
    return kếtQuảLờiGọi(jkoros_syscall(43, bộMôTảTệp, (int)DữLiệu, sốLượngByte, cácThiếtLập, (int)yêuCầu));
}
ssize_t recvfrom(int bộMôTảTệp, void *DữLiệu, size_t sốLượngByte, int cácThiếtLập,
                 struct sockaddr *địaChỉ, socklen_t *độDàiĐịaChỉ) {
    int yêuCầu[2] = {(int)địaChỉ, (int)độDàiĐịaChỉ};
    return kếtQuảLờiGọi(jkoros_syscall(44, bộMôTảTệp, (int)DữLiệu, sốLượngByte, cácThiếtLập, (int)yêuCầu));
}
int getsockname(int bộMôTảTệp, struct sockaddr *địaChỉ, socklen_t *độDàiĐịaChỉ) {
    return kếtQuảLờiGọi(jkoros_syscall(45, bộMôTảTệp, (int)địaChỉ, (int)độDàiĐịaChỉ, 0, 0));
}
int setsockopt(int bộMôTảTệp, int giáTrịTầng, int tênCácThiếtLập, const void *giáTrị, socklen_t độDàiGiáTrị) {
    if (giáTrịTầng != SOL_SOCKET || tênCácThiếtLập != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!giáTrị) { errno = EFAULT; return -1; }
    if (độDàiGiáTrị != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *giáTrịThờiGian = giáTrị;
    if (giáTrịThờiGian->tv_sec < 0 || giáTrịThờiGian->tv_sec > 2 || giáTrịThờiGian->tv_usec < 0 || giáTrịThờiGian->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int miliGiây = giáTrịThờiGian->tv_sec * 1000 + (giáTrịThờiGian->tv_usec + 999) / 1000;
    return kếtQuảLờiGọi(jkoros_syscall(46, bộMôTảTệp, miliGiây, 0, 0, 0));
}
uint16_t htons(uint16_t giáTrị) { return (giáTrị << 8) | (giáTrị >> 8); }
uint16_t ntohs(uint16_t giáTrị) { return htons(giáTrị); }
uint32_t htonl(uint32_t giáTrị) {
    return (giáTrị << 24) | ((giáTrị << 8) & 0xff0000U) | ((giáTrị >> 8) & 0xff00U) | (giáTrị >> 24);
}
uint32_t ntohl(uint32_t giáTrị) { return htonl(giáTrị); }
int inet_pton(int lượcĐồĐịaChỉ, const char *ChuỗiKýTự, void *địaChỉ) {
    if (lượcĐồĐịaChỉ != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ChuỗiKýTự || !địaChỉ) { errno = EFAULT; return -1; }
    unsigned char giáTrịTạm[4];
    for (int mụcÔ = 0; mụcÔ < 4; mụcÔ++) {
        int giáTrị = 0, cácChữSố = 0;
        const char *chạy = ChuỗiKýTự;
        while (*ChuỗiKýTự >= '0' && *ChuỗiKýTự <= '9') {
            if (++cácChữSố > 3) return 0;
            giáTrị = giáTrị * 10 + *ChuỗiKýTự++ - '0';
        }
        if (!cácChữSố || giáTrị > 255 || (cácChữSố > 1 && *chạy == '0')) return 0;
        giáTrịTạm[mụcÔ] = giáTrị;
        if (mụcÔ < 3) { if (*ChuỗiKýTự++ != '.') return 0; }
        else if (*ChuỗiKýTự) return 0;
    }
    for (int mụcÔ = 0; mụcÔ < 4; mụcÔ++) ((unsigned char *)địaChỉ)[mụcÔ] = giáTrịTạm[mụcÔ];
    return 1;
}
const char *inet_ntop(int lượcĐồĐịaChỉ, const void *địaChỉ, char *ChuỗiKýTự, socklen_t giáTrịSứcChứa) {
    if (lượcĐồĐịaChỉ != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!địaChỉ || !ChuỗiKýTự) { errno = EFAULT; return 0; }
    const unsigned char *trịSố = địaChỉ;
    char giáTrịTạm[16]; unsigned int độDài = 0;
    for (int mụcÔ = 0; mụcÔ < 4; mụcÔ++) {
        unsigned int giáTrị = trịSố[mụcÔ];
        if (giáTrị >= 100) giáTrịTạm[độDài++] = '0' + giáTrị / 100;
        if (giáTrị >= 10) giáTrịTạm[độDài++] = '0' + giáTrị / 10 % 10;
        giáTrịTạm[độDài++] = '0' + giáTrị % 10;
        if (mụcÔ < 3) giáTrịTạm[độDài++] = '.';
    }
    giáTrịTạm[độDài++] = 0;
    if (giáTrịSứcChứa < độDài) { errno = ENOSPC; return 0; }
    for (unsigned int mụcÔ = 0; mụcÔ < độDài; mụcÔ++) ChuỗiKýTự[mụcÔ] = giáTrịTạm[mụcÔ];
    return ChuỗiKýTự;
}
