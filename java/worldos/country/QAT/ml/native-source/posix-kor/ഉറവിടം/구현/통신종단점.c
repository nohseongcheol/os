#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ഇമെയിൽ, socklen_t ഇമെയിൽ_ദൈര്_ഘ്യം) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ഇമെയിൽ, ഇമെയിൽ_ദൈര്_ഘ്യം, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ഡാറ്റാ, size_t 바이트수, int സജ്ജീകരണം,
               const struct sockaddr *ഇമെയിൽ, socklen_t ഇമെയിൽ_ദൈര്_ഘ്യം) {
    int HTTP_അപേക്ഷ[2] = {(int)ഇമെയിൽ, ഇമെയിൽ_ദൈര്_ഘ്യം};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ഡാറ്റാ, 바이트수, സജ്ജീകരണം, (int)HTTP_അപേക്ഷ));
}
ssize_t recvfrom(int 파일서술자, void *ഡാറ്റാ, size_t 바이트수, int സജ്ജീകരണം,
                 struct sockaddr *ഇമെയിൽ, socklen_t *ഇമെയിൽ_ദൈര്_ഘ്യം) {
    int HTTP_അപേക്ഷ[2] = {(int)ഇമെയിൽ, (int)ഇമെയിൽ_ദൈര്_ഘ്യം};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ഡാറ്റാ, 바이트수, സജ്ജീകരണം, (int)HTTP_അപേക്ഷ));
}
int getsockname(int 파일서술자, struct sockaddr *ഇമെയിൽ, socklen_t *ഇമെയിൽ_ദൈര്_ഘ്യം) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ഇമെയിൽ, (int)ഇമെയിൽ_ദൈര്_ഘ്യം, 0, 0));
}
int setsockopt(int 파일서술자, int ലെയര്_മൂല്യം, int ക്രമീകരണം_നാ_മം, const void *മൂല്യം, socklen_t മൂല്യം_ദൈര്_ഘ്യം) {
    if (ലെയര്_മൂല്യം != SOL_SOCKET || ക്രമീകരണം_നാ_മം != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!മൂല്യം) { errno = EFAULT; return -1; }
    if (മൂല്യം_ദൈര്_ഘ്യം != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *സമയ_മൂല്യം = മൂല്യം;
    if (സമയ_മൂല്യം->tv_sec < 0 || സമയ_മൂല്യം->tv_sec > 2 || സമയ_മൂല്യം->tv_usec < 0 || സമയ_മൂല്യം->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = സമയ_മൂല്യം->tv_sec * 1000 + (സമയ_മൂല്യം->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t മൂല്യം) { return (മൂല്യം << 8) | (മൂല്യം >> 8); }
uint16_t ntohs(uint16_t മൂല്യം) { return htons(മൂല്യം); }
uint32_t htonl(uint32_t മൂല്യം) {
    return (മൂല്യം << 24) | ((മൂല്യം << 8) & 0xff0000U) | ((മൂല്യം >> 8) & 0xff00U) | (മൂല്യം >> 24);
}
uint32_t ntohl(uint32_t മൂല്യം) { return htonl(മൂല്യം); }
int inet_pton(int 주소체계, const char *സ്ട്രിംഗ്_മൂല്യം, void *ഇമെയിൽ) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!സ്ട്രിംഗ്_മൂല്യം || !ഇമെയിൽ) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int സ്ലോട്ട്_എന്_ട്രി = 0; സ്ലോട്ട്_എന്_ട്രി < 4; സ്ലോട്ട്_എന്_ട്രി++) {
        int മൂല്യം = 0, 자릿수 = 0;
        const char *നടപ്പിലാക്കുക = സ്ട്രിംഗ്_മൂല്യം;
        while (*സ്ട്രിംഗ്_മൂല്യം >= '0' && *സ്ട്രിംഗ്_മൂല്യം <= '9') {
            if (++자릿수 > 3) return 0;
            മൂല്യം = മൂല്യം * 10 + *സ്ട്രിംഗ്_മൂല്യം++ - '0';
        }
        if (!자릿수 || മൂല്യം > 255 || (자릿수 > 1 && *നടപ്പിലാക്കുക == '0')) return 0;
        임시[സ്ലോട്ട്_എന്_ട്രി] = മൂല്യം;
        if (സ്ലോട്ട്_എന്_ട്രി < 3) { if (*സ്ട്രിംഗ്_മൂല്യം++ != '.') return 0; }
        else if (*സ്ട്രിംഗ്_മൂല്യം) return 0;
    }
    for (int സ്ലോട്ട്_എന്_ട്രി = 0; സ്ലോട്ട്_എന്_ട്രി < 4; സ്ലോട്ട്_എന്_ട്രി++) ((unsigned char *)ഇമെയിൽ)[സ്ലോട്ട്_എന്_ട്രി] = 임시[സ്ലോട്ട്_എന്_ട്രി];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ഇമെയിൽ, char *സ്ട്രിംഗ്_മൂല്യം, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ഇമെയിൽ || !സ്ട്രിംഗ്_മൂല്യം) { errno = EFAULT; return 0; }
    const unsigned char *수 = ഇമെയിൽ;
    char 임시[16]; unsigned int ദൈര്_ഘ്യം_മൂല്യം = 0;
    for (int സ്ലോട്ട്_എന്_ട്രി = 0; സ്ലോട്ട്_എന്_ട്രി < 4; സ്ലോട്ട്_എന്_ട്രി++) {
        unsigned int മൂല്യം = 수[സ്ലോട്ട്_എന്_ട്രി];
        if (മൂല്യം >= 100) 임시[ദൈര്_ഘ്യം_മൂല്യം++] = '0' + മൂല്യം / 100;
        if (മൂല്യം >= 10) 임시[ദൈര്_ഘ്യം_മൂല്യം++] = '0' + മൂല്യം / 10 % 10;
        임시[ദൈര്_ഘ്യം_മൂല്യം++] = '0' + മൂല്യം % 10;
        if (സ്ലോട്ട്_എന്_ട്രി < 3) 임시[ദൈര്_ഘ്യം_മൂല്യം++] = '.';
    }
    임시[ദൈര്_ഘ്യം_മൂല്യം++] = 0;
    if (용량 < ദൈര്_ഘ്യം_മൂല്യം) { errno = ENOSPC; return 0; }
    for (unsigned int സ്ലോട്ട്_എന്_ട്രി = 0; സ്ലോട്ട്_എന്_ട്രി < ദൈര്_ഘ്യം_മൂല്യം; സ്ലോട്ട്_എന്_ട്രി++) സ്ട്രിംഗ്_മൂല്യം[സ്ലോട്ട്_എന്_ട്രി] = 임시[സ്ലോട്ട്_എന്_ട്രി];
    return സ്ട്രിംഗ്_മൂല്യം;
}
