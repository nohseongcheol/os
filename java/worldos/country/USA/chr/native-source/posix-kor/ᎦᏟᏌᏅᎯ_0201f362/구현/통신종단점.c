#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, socklen_t ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᏱᎦᏅᎯᏓ) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᏱᎦᏅᎯᏓ, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ᎦᏟᏌᏅᎯ, size_t 바이트수, int ᏕᎦᎧᎲᎢ,
               const struct sockaddr *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, socklen_t ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᏱᎦᏅᎯᏓ) {
    int 요청[2] = {(int)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᏱᎦᏅᎯᏓ};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ᎦᏟᏌᏅᎯ, 바이트수, ᏕᎦᎧᎲᎢ, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ᎦᏟᏌᏅᎯ, size_t 바이트수, int ᏕᎦᎧᎲᎢ,
                 struct sockaddr *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, socklen_t *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᏱᎦᏅᎯᏓ) {
    int 요청[2] = {(int)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, (int)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᏱᎦᏅᎯᏓ};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ᎦᏟᏌᏅᎯ, 바이트수, ᏕᎦᎧᎲᎢ, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, socklen_t *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᏱᎦᏅᎯᏓ) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, (int)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_ᏱᎦᏅᎯᏓ, 0, 0));
}
int setsockopt(int 파일서술자, int ᏗᏰᎦᏟ_ᏧᎬᏩᎶᏗᏯ, int ᏕᎦᎧᎲᎢ_ᏚᏙᎥᎢ, const void *ᏧᎬᏩᎶᏗᏯ, socklen_t ᏧᎬᏩᎶᏗᏯ_ᏱᎦᏅᎯᏓ) {
    if (ᏗᏰᎦᏟ_ᏧᎬᏩᎶᏗᏯ != SOL_SOCKET || ᏕᎦᎧᎲᎢ_ᏚᏙᎥᎢ != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ᏧᎬᏩᎶᏗᏯ) { errno = EFAULT; return -1; }
    if (ᏧᎬᏩᎶᏗᏯ_ᏱᎦᏅᎯᏓ != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = ᏧᎬᏩᎶᏗᏯ;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ᏧᎬᏩᎶᏗᏯ) { return (ᏧᎬᏩᎶᏗᏯ << 8) | (ᏧᎬᏩᎶᏗᏯ >> 8); }
uint16_t ntohs(uint16_t ᏧᎬᏩᎶᏗᏯ) { return htons(ᏧᎬᏩᎶᏗᏯ); }
uint32_t htonl(uint32_t ᏧᎬᏩᎶᏗᏯ) {
    return (ᏧᎬᏩᎶᏗᏯ << 24) | ((ᏧᎬᏩᎶᏗᏯ << 8) & 0xff0000U) | ((ᏧᎬᏩᎶᏗᏯ >> 8) & 0xff00U) | (ᏧᎬᏩᎶᏗᏯ >> 24);
}
uint32_t ntohl(uint32_t ᏧᎬᏩᎶᏗᏯ) { return htonl(ᏧᎬᏩᎶᏗᏯ); }
int inet_pton(int 주소체계, const char *ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ, void *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ || !ᎪᏪᎵ_ᏫᏗᎦᏅᏗ) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int ᏧᎬᏩᎶᏗᏯ = 0, 자릿수 = 0;
        const char *ᎠᎢᏎᏍᏗ = ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ;
        while (*ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ >= '0' && *ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ <= '9') {
            if (++자릿수 > 3) return 0;
            ᏧᎬᏩᎶᏗᏯ = ᏧᎬᏩᎶᏗᏯ * 10 + *ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ++ - '0';
        }
        if (!자릿수 || ᏧᎬᏩᎶᏗᏯ > 255 || (자릿수 > 1 && *ᎠᎢᏎᏍᏗ == '0')) return 0;
        임시[칸] = ᏧᎬᏩᎶᏗᏯ;
        if (칸 < 3) { if (*ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ++ != '.') return 0; }
        else if (*ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, char *ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ᎪᏪᎵ_ᏫᏗᎦᏅᏗ || !ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ) { errno = EFAULT; return 0; }
    const unsigned char *수 = ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;
    char 임시[16]; unsigned int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int ᏧᎬᏩᎶᏗᏯ = 수[칸];
        if (ᏧᎬᏩᎶᏗᏯ >= 100) 임시[ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ++] = '0' + ᏧᎬᏩᎶᏗᏯ / 100;
        if (ᏧᎬᏩᎶᏗᏯ >= 10) 임시[ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ++] = '0' + ᏧᎬᏩᎶᏗᏯ / 10 % 10;
        임시[ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ++] = '0' + ᏧᎬᏩᎶᏗᏯ % 10;
        if (칸 < 3) 임시[ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ++] = '.';
    }
    임시[ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ++] = 0;
    if (용량 < ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ; 칸++) ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ[칸] = 임시[칸];
    return ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ;
}
