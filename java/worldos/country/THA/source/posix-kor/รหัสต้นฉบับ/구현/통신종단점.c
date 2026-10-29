#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int กรณี_หมายเลข) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, กรณี_หมายเลข, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *อีเมล, socklen_t 주소길이) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)อีเมล, 주소길이, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ข้อมูล, size_t 바이트수, int ตั้งค่า,
               const struct sockaddr *อีเมล, socklen_t 주소길이) {
    int คําขอ[2] = {(int)อีเมล, 주소길이};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ข้อมูล, 바이트수, ตั้งค่า, (int)คําขอ));
}
ssize_t recvfrom(int 파일서술자, void *ข้อมูล, size_t 바이트수, int ตั้งค่า,
                 struct sockaddr *อีเมล, socklen_t *주소길이) {
    int คําขอ[2] = {(int)อีเมล, (int)주소길이};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ข้อมูล, 바이트수, ตั้งค่า, (int)คําขอ));
}
int getsockname(int 파일서술자, struct sockaddr *อีเมล, socklen_t *주소길이) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)อีเมล, (int)주소길이, 0, 0));
}
int setsockopt(int 파일서술자, int เลเยอร์_ค่า, int การตั้งค่า_ชื่อ, const void *ค่า, socklen_t 값길이) {
    if (เลเยอร์_ค่า != SOL_SOCKET || การตั้งค่า_ชื่อ != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ค่า) { errno = EFAULT; return -1; }
    if (값길이 != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *ค่าเวลา = ค่า;
    if (ค่าเวลา->tv_sec < 0 || ค่าเวลา->tv_sec > 2 || ค่าเวลา->tv_usec < 0 || ค่าเวลา->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = ค่าเวลา->tv_sec * 1000 + (ค่าเวลา->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ค่า) { return (ค่า << 8) | (ค่า >> 8); }
uint16_t ntohs(uint16_t ค่า) { return htons(ค่า); }
uint32_t htonl(uint32_t ค่า) {
    return (ค่า << 24) | ((ค่า << 8) & 0xff0000U) | ((ค่า >> 8) & 0xff00U) | (ค่า >> 24);
}
uint32_t ntohl(uint32_t ค่า) { return htonl(ค่า); }
int inet_pton(int 주소체계, const char *สตริง_ค่า, void *อีเมล) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!สตริง_ค่า || !อีเมล) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int ค่า = 0, 자릿수 = 0;
        const char *เรียกใช้งาน = สตริง_ค่า;
        while (*สตริง_ค่า >= '0' && *สตริง_ค่า <= '9') {
            if (++자릿수 > 3) return 0;
            ค่า = ค่า * 10 + *สตริง_ค่า++ - '0';
        }
        if (!자릿수 || ค่า > 255 || (자릿수 > 1 && *เรียกใช้งาน == '0')) return 0;
        임시[칸] = ค่า;
        if (칸 < 3) { if (*สตริง_ค่า++ != '.') return 0; }
        else if (*สตริง_ค่า) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)อีเมล)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *อีเมล, char *สตริง_ค่า, socklen_t ความจุ_ค่า) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!อีเมล || !สตริง_ค่า) { errno = EFAULT; return 0; }
    const unsigned char *หมายเลข = อีเมล;
    char 임시[16]; unsigned int 길이 = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int ค่า = หมายเลข[칸];
        if (ค่า >= 100) 임시[길이++] = '0' + ค่า / 100;
        if (ค่า >= 10) 임시[길이++] = '0' + ค่า / 10 % 10;
        임시[길이++] = '0' + ค่า % 10;
        if (칸 < 3) 임시[길이++] = '.';
    }
    임시[길이++] = 0;
    if (ความจุ_ค่า < 길이) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < 길이; 칸++) สตริง_ค่า[칸] = 임시[칸];
    return สตริง_ค่า;
}
