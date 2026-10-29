#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ইমেইল, socklen_t ইমেইল_দৈর্ঘ্য) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ইমেইল, ইমেইল_দৈর্ঘ্য, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ডাটা, size_t 바이트수, int সেটিংস,
               const struct sockaddr *ইমেইল, socklen_t ইমেইল_দৈর্ঘ্য) {
    int 요청[2] = {(int)ইমেইল, ইমেইল_দৈর্ঘ্য};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ডাটা, 바이트수, সেটিংস, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ডাটা, size_t 바이트수, int সেটিংস,
                 struct sockaddr *ইমেইল, socklen_t *ইমেইল_দৈর্ঘ্য) {
    int 요청[2] = {(int)ইমেইল, (int)ইমেইল_দৈর্ঘ্য};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ডাটা, 바이트수, সেটিংস, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ইমেইল, socklen_t *ইমেইল_দৈর্ঘ্য) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ইমেইল, (int)ইমেইল_দৈর্ঘ্য, 0, 0));
}
int setsockopt(int 파일서술자, int স্তর_মান, int সেটিংস_নাম, const void *মান, socklen_t মান_দৈর্ঘ্য) {
    if (স্তর_মান != SOL_SOCKET || সেটিংস_নাম != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!মান) { errno = EFAULT; return -1; }
    if (মান_দৈর্ঘ্য != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *সময়_মান = মান;
    if (সময়_মান->tv_sec < 0 || সময়_মান->tv_sec > 2 || সময়_মান->tv_usec < 0 || সময়_মান->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = সময়_মান->tv_sec * 1000 + (সময়_মান->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t মান) { return (মান << 8) | (মান >> 8); }
uint16_t ntohs(uint16_t মান) { return htons(মান); }
uint32_t htonl(uint32_t মান) {
    return (মান << 24) | ((মান << 8) & 0xff0000U) | ((মান >> 8) & 0xff00U) | (মান >> 24);
}
uint32_t ntohl(uint32_t মান) { return htonl(মান); }
int inet_pton(int 주소체계, const char *স্ট্রিং_মান, void *ইমেইল) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!স্ট্রিং_মান || !ইমেইল) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int স্লট_ভুক্তি = 0; স্লট_ভুক্তি < 4; স্লট_ভুক্তি++) {
        int মান = 0, 자릿수 = 0;
        const char *চালনা = স্ট্রিং_মান;
        while (*স্ট্রিং_মান >= '0' && *স্ট্রিং_মান <= '9') {
            if (++자릿수 > 3) return 0;
            মান = মান * 10 + *স্ট্রিং_মান++ - '0';
        }
        if (!자릿수 || মান > 255 || (자릿수 > 1 && *চালনা == '0')) return 0;
        임시[স্লট_ভুক্তি] = মান;
        if (স্লট_ভুক্তি < 3) { if (*স্ট্রিং_মান++ != '.') return 0; }
        else if (*স্ট্রিং_মান) return 0;
    }
    for (int স্লট_ভুক্তি = 0; স্লট_ভুক্তি < 4; স্লট_ভুক্তি++) ((unsigned char *)ইমেইল)[স্লট_ভুক্তি] = 임시[স্লট_ভুক্তি];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ইমেইল, char *স্ট্রিং_মান, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ইমেইল || !স্ট্রিং_মান) { errno = EFAULT; return 0; }
    const unsigned char *수 = ইমেইল;
    char 임시[16]; unsigned int দৈর্ঘ্য_মান = 0;
    for (int স্লট_ভুক্তি = 0; স্লট_ভুক্তি < 4; স্লট_ভুক্তি++) {
        unsigned int মান = 수[স্লট_ভুক্তি];
        if (মান >= 100) 임시[দৈর্ঘ্য_মান++] = '0' + মান / 100;
        if (মান >= 10) 임시[দৈর্ঘ্য_মান++] = '0' + মান / 10 % 10;
        임시[দৈর্ঘ্য_মান++] = '0' + মান % 10;
        if (স্লট_ভুক্তি < 3) 임시[দৈর্ঘ্য_মান++] = '.';
    }
    임시[দৈর্ঘ্য_মান++] = 0;
    if (용량 < দৈর্ঘ্য_মান) { errno = ENOSPC; return 0; }
    for (unsigned int স্লট_ভুক্তি = 0; স্লট_ভুক্তি < দৈর্ঘ্য_মান; স্লট_ভুক্তি++) স্ট্রিং_মান[স্লট_ভুক্তি] = 임시[স্লট_ভুক্তি];
    return স্ট্রিং_মান;
}
