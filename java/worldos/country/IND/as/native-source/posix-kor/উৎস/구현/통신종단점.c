#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ঠিকনা, socklen_t ঠিকনা_দৈর্ঘ্য) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ঠিকনা, ঠিকনা_দৈর্ঘ্য, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ডাটা, size_t 바이트수, int বৈশিষ্ট্য,
               const struct sockaddr *ঠিকনা, socklen_t ঠিকনা_দৈর্ঘ্য) {
    int 요청[2] = {(int)ঠিকনা, ঠিকনা_দৈর্ঘ্য};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ডাটা, 바이트수, বৈশিষ্ট্য, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ডাটা, size_t 바이트수, int বৈশিষ্ট্য,
                 struct sockaddr *ঠিকনা, socklen_t *ঠিকনা_দৈর্ঘ্য) {
    int 요청[2] = {(int)ঠিকনা, (int)ঠিকনা_দৈর্ঘ্য};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ডাটা, 바이트수, বৈশিষ্ট্য, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ঠিকনা, socklen_t *ঠিকনা_দৈর্ঘ্য) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ঠিকনা, (int)ঠিকনা_দৈর্ঘ্য, 0, 0));
}
int setsockopt(int 파일서술자, int তৰপ_মান, int ছেটিংছ_নাম, const void *মান, socklen_t মান_দৈর্ঘ্য) {
    if (তৰপ_মান != SOL_SOCKET || ছেটিংছ_নাম != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!মান) { errno = EFAULT; return -1; }
    if (মান_দৈর্ঘ্য != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = মান;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t মান) { return (মান << 8) | (মান >> 8); }
uint16_t ntohs(uint16_t মান) { return htons(মান); }
uint32_t htonl(uint32_t মান) {
    return (মান << 24) | ((মান << 8) & 0xff0000U) | ((মান >> 8) & 0xff00U) | (মান >> 24);
}
uint32_t ntohl(uint32_t মান) { return htonl(মান); }
int inet_pton(int 주소체계, const char *ষ্ট্ৰিং_মান, void *ঠিকনা) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ষ্ট্ৰিং_মান || !ঠিকনা) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int শ্লট_প্রবিষ্ট = 0; শ্লট_প্রবিষ্ট < 4; শ্লট_প্রবিষ্ট++) {
        int মান = 0, 자릿수 = 0;
        const char *সঞ্চালন = ষ্ট্ৰিং_মান;
        while (*ষ্ট্ৰিং_মান >= '0' && *ষ্ট্ৰিং_মান <= '9') {
            if (++자릿수 > 3) return 0;
            মান = মান * 10 + *ষ্ট্ৰিং_মান++ - '0';
        }
        if (!자릿수 || মান > 255 || (자릿수 > 1 && *সঞ্চালন == '0')) return 0;
        임시[শ্লট_প্রবিষ্ট] = মান;
        if (শ্লট_প্রবিষ্ট < 3) { if (*ষ্ট্ৰিং_মান++ != '.') return 0; }
        else if (*ষ্ট্ৰিং_মান) return 0;
    }
    for (int শ্লট_প্রবিষ্ট = 0; শ্লট_প্রবিষ্ট < 4; শ্লট_প্রবিষ্ট++) ((unsigned char *)ঠিকনা)[শ্লট_প্রবিষ্ট] = 임시[শ্লট_প্রবিষ্ট];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ঠিকনা, char *ষ্ট্ৰিং_মান, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ঠিকনা || !ষ্ট্ৰিং_মান) { errno = EFAULT; return 0; }
    const unsigned char *수 = ঠিকনা;
    char 임시[16]; unsigned int দৈর্ঘ্য_মান = 0;
    for (int শ্লট_প্রবিষ্ট = 0; শ্লট_প্রবিষ্ট < 4; শ্লট_প্রবিষ্ট++) {
        unsigned int মান = 수[শ্লট_প্রবিষ্ট];
        if (মান >= 100) 임시[দৈর্ঘ্য_মান++] = '0' + মান / 100;
        if (মান >= 10) 임시[দৈর্ঘ্য_মান++] = '0' + মান / 10 % 10;
        임시[দৈর্ঘ্য_মান++] = '0' + মান % 10;
        if (শ্লট_প্রবিষ্ট < 3) 임시[দৈর্ঘ্য_মান++] = '.';
    }
    임시[দৈর্ঘ্য_মান++] = 0;
    if (용량 < দৈর্ঘ্য_মান) { errno = ENOSPC; return 0; }
    for (unsigned int শ্লট_প্রবিষ্ট = 0; শ্লট_প্রবিষ্ট < দৈর্ঘ্য_মান; শ্লট_প্রবিষ্ট++) ষ্ট্ৰিং_মান[শ্লট_প্রবিষ্ট] = 임시[শ্লট_প্রবিষ্ট];
    return ষ্ট্ৰিং_মান;
}
