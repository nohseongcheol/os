#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *дарек, socklen_t дарек_узундук) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)дарек, дарек_узундук, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *берилмелер, size_t 바이트수, int Орнотуулар,
               const struct sockaddr *дарек, socklen_t дарек_узундук) {
    int 요청[2] = {(int)дарек, дарек_узундук};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)берилмелер, 바이트수, Орнотуулар, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *берилмелер, size_t 바이트수, int Орнотуулар,
                 struct sockaddr *дарек, socklen_t *дарек_узундук) {
    int 요청[2] = {(int)дарек, (int)дарек_узундук};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)берилмелер, 바이트수, Орнотуулар, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *дарек, socklen_t *дарек_узундук) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)дарек, (int)дарек_узундук, 0, 0));
}
int setsockopt(int 파일서술자, int катмар_маани, int Орнотуулар_аты, const void *маани, socklen_t маани_узундук) {
    if (катмар_маани != SOL_SOCKET || Орнотуулар_аты != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!маани) { errno = EFAULT; return -1; }
    if (маани_узундук != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = маани;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t маани) { return (маани << 8) | (маани >> 8); }
uint16_t ntohs(uint16_t маани) { return htons(маани); }
uint32_t htonl(uint32_t маани) {
    return (маани << 24) | ((маани << 8) & 0xff0000U) | ((маани >> 8) & 0xff00U) | (маани >> 24);
}
uint32_t ntohl(uint32_t маани) { return htonl(маани); }
int inet_pton(int 주소체계, const char *сап_маани, void *дарек) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!сап_маани || !дарек) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int оюкча_киргизме_жазуу = 0; оюкча_киргизме_жазуу < 4; оюкча_киргизме_жазуу++) {
        int маани = 0, 자릿수 = 0;
        const char *Жүргүзүү = сап_маани;
        while (*сап_маани >= '0' && *сап_маани <= '9') {
            if (++자릿수 > 3) return 0;
            маани = маани * 10 + *сап_маани++ - '0';
        }
        if (!자릿수 || маани > 255 || (자릿수 > 1 && *Жүргүзүү == '0')) return 0;
        임시[оюкча_киргизме_жазуу] = маани;
        if (оюкча_киргизме_жазуу < 3) { if (*сап_маани++ != '.') return 0; }
        else if (*сап_маани) return 0;
    }
    for (int оюкча_киргизме_жазуу = 0; оюкча_киргизме_жазуу < 4; оюкча_киргизме_жазуу++) ((unsigned char *)дарек)[оюкча_киргизме_жазуу] = 임시[оюкча_киргизме_жазуу];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *дарек, char *сап_маани, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!дарек || !сап_маани) { errno = EFAULT; return 0; }
    const unsigned char *수 = дарек;
    char 임시[16]; unsigned int узундук_маани = 0;
    for (int оюкча_киргизме_жазуу = 0; оюкча_киргизме_жазуу < 4; оюкча_киргизме_жазуу++) {
        unsigned int маани = 수[оюкча_киргизме_жазуу];
        if (маани >= 100) 임시[узундук_маани++] = '0' + маани / 100;
        if (маани >= 10) 임시[узундук_маани++] = '0' + маани / 10 % 10;
        임시[узундук_маани++] = '0' + маани % 10;
        if (оюкча_киргизме_жазуу < 3) 임시[узундук_маани++] = '.';
    }
    임시[узундук_маани++] = 0;
    if (용량 < узундук_маани) { errno = ENOSPC; return 0; }
    for (unsigned int оюкча_киргизме_жазуу = 0; оюкча_киргизме_жазуу < узундук_маани; оюкча_киргизме_жазуу++) сап_маани[оюкча_киргизме_жазуу] = 임시[оюкча_киргизме_жазуу];
    return сап_маани;
}
