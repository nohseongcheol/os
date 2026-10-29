#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int عقد_رقم) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, عقد_رقم, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *عنوان, socklen_t 주소길이) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)عنوان, 주소길이, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *بيانات, size_t 바이트수, int إعدادات,
               const struct sockaddr *عنوان, socklen_t 주소길이) {
    int طلب[2] = {(int)عنوان, 주소길이};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)بيانات, 바이트수, إعدادات, (int)طلب));
}
ssize_t recvfrom(int 파일서술자, void *بيانات, size_t 바이트수, int إعدادات,
                 struct sockaddr *عنوان, socklen_t *주소길이) {
    int طلب[2] = {(int)عنوان, (int)주소길이};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)بيانات, 바이트수, إعدادات, (int)طلب));
}
int getsockname(int 파일서술자, struct sockaddr *عنوان, socklen_t *주소길이) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)عنوان, (int)주소길이, 0, 0));
}
int setsockopt(int 파일서술자, int طبقة_قيمة, int إعدادات_اسم, const void *قيمة, socklen_t 값길이) {
    if (طبقة_قيمة != SOL_SOCKET || إعدادات_اسم != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!قيمة) { errno = EFAULT; return -1; }
    if (값길이 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *قيمة_الوقت = قيمة;
    if (قيمة_الوقت->tv_sec < 0 || قيمة_الوقت->tv_sec > 2 || قيمة_الوقت->tv_usec < 0 || قيمة_الوقت->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = قيمة_الوقت->tv_sec * 1000 + (قيمة_الوقت->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t قيمة) { return (قيمة << 8) | (قيمة >> 8); }
uint16_t ntohs(uint16_t قيمة) { return htons(قيمة); }
uint32_t htonl(uint32_t قيمة) {
    return (قيمة << 24) | ((قيمة << 8) & 0xff0000U) | ((قيمة >> 8) & 0xff00U) | (قيمة >> 24);
}
uint32_t ntohl(uint32_t قيمة) { return htonl(قيمة); }
int inet_pton(int 주소체계, const char *سلسلة_قيمة, void *عنوان) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!سلسلة_قيمة || !عنوان) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int فتحة_إدخال = 0; فتحة_إدخال < 4; فتحة_إدخال++) {
        int قيمة = 0, 자릿수 = 0;
        const char *تشغيل = سلسلة_قيمة;
        while (*سلسلة_قيمة >= '0' && *سلسلة_قيمة <= '9') {
            if (++자릿수 > 3) return 0;
            قيمة = قيمة * 10 + *سلسلة_قيمة++ - '0';
        }
        if (!자릿수 || قيمة > 255 || (자릿수 > 1 && *تشغيل == '0')) return 0;
        임시[فتحة_إدخال] = قيمة;
        if (فتحة_إدخال < 3) { if (*سلسلة_قيمة++ != '.') return 0; }
        else if (*سلسلة_قيمة) return 0;
    }
    for (int فتحة_إدخال = 0; فتحة_إدخال < 4; فتحة_إدخال++) ((unsigned char *)عنوان)[فتحة_إدخال] = 임시[فتحة_إدخال];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *عنوان, char *سلسلة_قيمة, socklen_t قدرة_قيمة) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!عنوان || !سلسلة_قيمة) { errno = EFAULT; return 0; }
    const unsigned char *رقم = عنوان;
    char 임시[16]; unsigned int 길이 = 0;
    for (int فتحة_إدخال = 0; فتحة_إدخال < 4; فتحة_إدخال++) {
        unsigned int قيمة = رقم[فتحة_إدخال];
        if (قيمة >= 100) 임시[길이++] = '0' + قيمة / 100;
        if (قيمة >= 10) 임시[길이++] = '0' + قيمة / 10 % 10;
        임시[길이++] = '0' + قيمة % 10;
        if (فتحة_إدخال < 3) 임시[길이++] = '.';
    }
    임시[길이++] = 0;
    if (قدرة_قيمة < 길이) { errno = ENOSPC; return 0; }
    for (unsigned int فتحة_إدخال = 0; فتحة_إدخال < 길이; فتحة_إدخال++) سلسلة_قيمة[فتحة_إدخال] = 임시[فتحة_إدخال];
    return سلسلة_قيمة;
}
