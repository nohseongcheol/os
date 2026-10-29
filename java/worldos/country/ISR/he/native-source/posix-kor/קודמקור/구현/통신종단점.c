#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *למען, socklen_t 주소길이) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)למען, 주소길이, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *נתונים, size_t 바이트수, int הגדרות,
               const struct sockaddr *למען, socklen_t 주소길이) {
    int בקשה[2] = {(int)למען, 주소길이};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)נתונים, 바이트수, הגדרות, (int)בקשה));
}
ssize_t recvfrom(int 파일서술자, void *נתונים, size_t 바이트수, int הגדרות,
                 struct sockaddr *למען, socklen_t *주소길이) {
    int בקשה[2] = {(int)למען, (int)주소길이};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)נתונים, 바이트수, הגדרות, (int)בקשה));
}
int getsockname(int 파일서술자, struct sockaddr *למען, socklen_t *주소길이) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)למען, (int)주소길이, 0, 0));
}
int setsockopt(int 파일서술자, int שכבה_ערך, int הגדרות_שם, const void *ערך, socklen_t 값길이) {
    if (שכבה_ערך != SOL_SOCKET || הגדרות_שם != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ערך) { errno = EFAULT; return -1; }
    if (값길이 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *ערך_זמן = ערך;
    if (ערך_זמן->tv_sec < 0 || ערך_זמן->tv_sec > 2 || ערך_זמן->tv_usec < 0 || ערך_זמן->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = ערך_זמן->tv_sec * 1000 + (ערך_זמן->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ערך) { return (ערך << 8) | (ערך >> 8); }
uint16_t ntohs(uint16_t ערך) { return htons(ערך); }
uint32_t htonl(uint32_t ערך) {
    return (ערך << 24) | ((ערך << 8) & 0xff0000U) | ((ערך >> 8) & 0xff00U) | (ערך >> 24);
}
uint32_t ntohl(uint32_t ערך) { return htonl(ערך); }
int inet_pton(int 주소체계, const char *מחרוזת_ערך, void *למען) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!מחרוזת_ערך || !למען) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int חריץ_ערך = 0; חריץ_ערך < 4; חריץ_ערך++) {
        int ערך = 0, 자릿수 = 0;
        const char *הפעלה = מחרוזת_ערך;
        while (*מחרוזת_ערך >= '0' && *מחרוזת_ערך <= '9') {
            if (++자릿수 > 3) return 0;
            ערך = ערך * 10 + *מחרוזת_ערך++ - '0';
        }
        if (!자릿수 || ערך > 255 || (자릿수 > 1 && *הפעלה == '0')) return 0;
        임시[חריץ_ערך] = ערך;
        if (חריץ_ערך < 3) { if (*מחרוזת_ערך++ != '.') return 0; }
        else if (*מחרוזת_ערך) return 0;
    }
    for (int חריץ_ערך = 0; חריץ_ערך < 4; חריץ_ערך++) ((unsigned char *)למען)[חריץ_ערך] = 임시[חריץ_ערך];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *למען, char *מחרוזת_ערך, socklen_t קיבולת_ערך) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!למען || !מחרוזת_ערך) { errno = EFAULT; return 0; }
    const unsigned char *수 = למען;
    char 임시[16]; unsigned int 길이 = 0;
    for (int חריץ_ערך = 0; חריץ_ערך < 4; חריץ_ערך++) {
        unsigned int ערך = 수[חריץ_ערך];
        if (ערך >= 100) 임시[길이++] = '0' + ערך / 100;
        if (ערך >= 10) 임시[길이++] = '0' + ערך / 10 % 10;
        임시[길이++] = '0' + ערך % 10;
        if (חריץ_ערך < 3) 임시[길이++] = '.';
    }
    임시[길이++] = 0;
    if (קיבולת_ערך < 길이) { errno = ENOSPC; return 0; }
    for (unsigned int חריץ_ערך = 0; חריץ_ערך < 길이; חריץ_ערך++) מחרוזת_ערך[חריץ_ערך] = 임시[חריץ_ערך];
    return מחרוזת_ערך;
}
