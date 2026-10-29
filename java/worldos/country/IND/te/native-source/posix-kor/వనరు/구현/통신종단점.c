#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ఇమెయిల్, socklen_t ఇమెయిల్_పొడవు) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ఇమెయిల్, ఇమెయిల్_పొడవు, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *డేటా, size_t 바이트수, int అమరికలు,
               const struct sockaddr *ఇమెయిల్, socklen_t ఇమెయిల్_పొడవు) {
    int 요청[2] = {(int)ఇమెయిల్, ఇమెయిల్_పొడవు};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)డేటా, 바이트수, అమరికలు, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *డేటా, size_t 바이트수, int అమరికలు,
                 struct sockaddr *ఇమెయిల్, socklen_t *ఇమెయిల్_పొడవు) {
    int 요청[2] = {(int)ఇమెయిల్, (int)ఇమెయిల్_పొడవు};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)డేటా, 바이트수, అమరికలు, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ఇమెయిల్, socklen_t *ఇమెయిల్_పొడవు) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ఇమెయిల్, (int)ఇమెయిల్_పొడవు, 0, 0));
}
int setsockopt(int 파일서술자, int పొర_మూల్యం, int సెట్టింగ్_లు_పేరు, const void *మూల్యం, socklen_t మూల్యం_పొడవు) {
    if (పొర_మూల్యం != SOL_SOCKET || సెట్టింగ్_లు_పేరు != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!మూల్యం) { errno = EFAULT; return -1; }
    if (మూల్యం_పొడవు != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *సమయం_మూల్యం = మూల్యం;
    if (సమయం_మూల్యం->tv_sec < 0 || సమయం_మూల్యం->tv_sec > 2 || సమయం_మూల్యం->tv_usec < 0 || సమయం_మూల్యం->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = సమయం_మూల్యం->tv_sec * 1000 + (సమయం_మూల్యం->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t మూల్యం) { return (మూల్యం << 8) | (మూల్యం >> 8); }
uint16_t ntohs(uint16_t మూల్యం) { return htons(మూల్యం); }
uint32_t htonl(uint32_t మూల్యం) {
    return (మూల్యం << 24) | ((మూల్యం << 8) & 0xff0000U) | ((మూల్యం >> 8) & 0xff00U) | (మూల్యం >> 24);
}
uint32_t ntohl(uint32_t మూల్యం) { return htonl(మూల్యం); }
int inet_pton(int 주소체계, const char *అక్షరసరం_మూల్యం, void *ఇమెయిల్) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!అక్షరసరం_మూల్యం || !ఇమెయిల్) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int స్లాట్_ప్రవేశం = 0; స్లాట్_ప్రవేశం < 4; స్లాట్_ప్రవేశం++) {
        int మూల్యం = 0, 자릿수 = 0;
        const char *నడుపుము = అక్షరసరం_మూల్యం;
        while (*అక్షరసరం_మూల్యం >= '0' && *అక్షరసరం_మూల్యం <= '9') {
            if (++자릿수 > 3) return 0;
            మూల్యం = మూల్యం * 10 + *అక్షరసరం_మూల్యం++ - '0';
        }
        if (!자릿수 || మూల్యం > 255 || (자릿수 > 1 && *నడుపుము == '0')) return 0;
        임시[స్లాట్_ప్రవేశం] = మూల్యం;
        if (స్లాట్_ప్రవేశం < 3) { if (*అక్షరసరం_మూల్యం++ != '.') return 0; }
        else if (*అక్షరసరం_మూల్యం) return 0;
    }
    for (int స్లాట్_ప్రవేశం = 0; స్లాట్_ప్రవేశం < 4; స్లాట్_ప్రవేశం++) ((unsigned char *)ఇమెయిల్)[స్లాట్_ప్రవేశం] = 임시[స్లాట్_ప్రవేశం];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ఇమెయిల్, char *అక్షరసరం_మూల్యం, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ఇమెయిల్ || !అక్షరసరం_మూల్యం) { errno = EFAULT; return 0; }
    const unsigned char *수 = ఇమెయిల్;
    char 임시[16]; unsigned int పొడవు_మూల్యం = 0;
    for (int స్లాట్_ప్రవేశం = 0; స్లాట్_ప్రవేశం < 4; స్లాట్_ప్రవేశం++) {
        unsigned int మూల్యం = 수[స్లాట్_ప్రవేశం];
        if (మూల్యం >= 100) 임시[పొడవు_మూల్యం++] = '0' + మూల్యం / 100;
        if (మూల్యం >= 10) 임시[పొడవు_మూల్యం++] = '0' + మూల్యం / 10 % 10;
        임시[పొడవు_మూల్యం++] = '0' + మూల్యం % 10;
        if (స్లాట్_ప్రవేశం < 3) 임시[పొడవు_మూల్యం++] = '.';
    }
    임시[పొడవు_మూల్యం++] = 0;
    if (용량 < పొడవు_మూల్యం) { errno = ENOSPC; return 0; }
    for (unsigned int స్లాట్_ప్రవేశం = 0; స్లాట్_ప్రవేశం < పొడవు_మూల్యం; స్లాట్_ప్రవేశం++) అక్షరసరం_మూల్యం[స్లాట్_ప్రవేశం] = 임시[స్లాట్_ప్రవేశం];
    return అక్షరసరం_మూల్యం;
}
