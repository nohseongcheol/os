#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *អ៊ីម៉ែល, socklen_t អ៊ីម៉ែល_ប្រវែង) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)អ៊ីម៉ែល, អ៊ីម៉ែល_ប្រវែង, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ទិន្នន័យ, size_t 바이트수, int ការកំណត់,
               const struct sockaddr *អ៊ីម៉ែល, socklen_t អ៊ីម៉ែល_ប្រវែង) {
    int 요청[2] = {(int)អ៊ីម៉ែល, អ៊ីម៉ែល_ប្រវែង};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ទិន្នន័យ, 바이트수, ការកំណត់, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ទិន្នន័យ, size_t 바이트수, int ការកំណត់,
                 struct sockaddr *អ៊ីម៉ែល, socklen_t *អ៊ីម៉ែល_ប្រវែង) {
    int 요청[2] = {(int)អ៊ីម៉ែល, (int)អ៊ីម៉ែល_ប្រវែង};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ទិន្នន័យ, 바이트수, ការកំណត់, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *អ៊ីម៉ែល, socklen_t *អ៊ីម៉ែល_ប្រវែង) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)អ៊ីម៉ែល, (int)អ៊ីម៉ែល_ប្រវែង, 0, 0));
}
int setsockopt(int 파일서술자, int ស្រទាប់_តំលៃ, int ការកំណត់_ឈ្មោះ, const void *តំលៃ, socklen_t តំលៃ_ប្រវែង) {
    if (ស្រទាប់_តំលៃ != SOL_SOCKET || ការកំណត់_ឈ្មោះ != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!តំលៃ) { errno = EFAULT; return -1; }
    if (តំលៃ_ប្រវែង != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *ពេល_វេលា_តំលៃ = តំលៃ;
    if (ពេល_វេលា_តំលៃ->tv_sec < 0 || ពេល_វេលា_តំលៃ->tv_sec > 2 || ពេល_វេលា_តំលៃ->tv_usec < 0 || ពេល_វេលា_តំលៃ->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = ពេល_វេលា_តំលៃ->tv_sec * 1000 + (ពេល_វេលា_តំលៃ->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t តំលៃ) { return (តំលៃ << 8) | (តំលៃ >> 8); }
uint16_t ntohs(uint16_t តំលៃ) { return htons(តំលៃ); }
uint32_t htonl(uint32_t តំលៃ) {
    return (តំលៃ << 24) | ((តំលៃ << 8) & 0xff0000U) | ((តំលៃ >> 8) & 0xff00U) | (តំលៃ >> 24);
}
uint32_t ntohl(uint32_t តំលៃ) { return htonl(តំលៃ); }
int inet_pton(int 주소체계, const char *សំនុំអក្សរ_តំលៃ, void *អ៊ីម៉ែល) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!សំនុំអក្សរ_តំលៃ || !អ៊ីម៉ែល) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int ចន្លោះប្រហោង_ការបញ្ចូល = 0; ចន្លោះប្រហោង_ការបញ្ចូល < 4; ចន្លោះប្រហោង_ការបញ្ចូល++) {
        int តំលៃ = 0, 자릿수 = 0;
        const char *រត់ = សំនុំអក្សរ_តំលៃ;
        while (*សំនុំអក្សរ_តំលៃ >= '0' && *សំនុំអក្សរ_តំលៃ <= '9') {
            if (++자릿수 > 3) return 0;
            តំលៃ = តំលៃ * 10 + *សំនុំអក្សរ_តំលៃ++ - '0';
        }
        if (!자릿수 || តំលៃ > 255 || (자릿수 > 1 && *រត់ == '0')) return 0;
        임시[ចន្លោះប្រហោង_ការបញ្ចូល] = តំលៃ;
        if (ចន្លោះប្រហោង_ការបញ្ចូល < 3) { if (*សំនុំអក្សរ_តំលៃ++ != '.') return 0; }
        else if (*សំនុំអក្សរ_តំលៃ) return 0;
    }
    for (int ចន្លោះប្រហោង_ការបញ្ចូល = 0; ចន្លោះប្រហោង_ការបញ្ចូល < 4; ចន្លោះប្រហោង_ការបញ្ចូល++) ((unsigned char *)អ៊ីម៉ែល)[ចន្លោះប្រហោង_ការបញ្ចូល] = 임시[ចន្លោះប្រហោង_ការបញ្ចូល];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *អ៊ីម៉ែល, char *សំនុំអក្សរ_តំលៃ, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!អ៊ីម៉ែល || !សំនុំអក្សរ_តំលៃ) { errno = EFAULT; return 0; }
    const unsigned char *수 = អ៊ីម៉ែល;
    char 임시[16]; unsigned int ប្រវែង_តំលៃ = 0;
    for (int ចន្លោះប្រហោង_ការបញ្ចូល = 0; ចន្លោះប្រហោង_ការបញ្ចូល < 4; ចន្លោះប្រហោង_ការបញ្ចូល++) {
        unsigned int តំលៃ = 수[ចន្លោះប្រហោង_ការបញ្ចូល];
        if (តំលៃ >= 100) 임시[ប្រវែង_តំលៃ++] = '0' + តំលៃ / 100;
        if (តំលៃ >= 10) 임시[ប្រវែង_តំលៃ++] = '0' + តំលៃ / 10 % 10;
        임시[ប្រវែង_តំលៃ++] = '0' + តំលៃ % 10;
        if (ចន្លោះប្រហោង_ការបញ្ចូល < 3) 임시[ប្រវែង_តំលៃ++] = '.';
    }
    임시[ប្រវែង_តំលៃ++] = 0;
    if (용량 < ប្រវែង_តំលៃ) { errno = ENOSPC; return 0; }
    for (unsigned int ចន្លោះប្រហោង_ការបញ្ចូល = 0; ចន្លោះប្រហោង_ការបញ្ចូល < ប្រវែង_តំលៃ; ចន្លោះប្រហោង_ការបញ្ចូល++) សំនុំអក្សរ_តំលៃ[ចន្លោះប្រហោង_ការបញ្ចូល] = 임시[ចន្លោះប្រហោង_ការបញ្ចូល];
    return សំនុំអក្សរ_តំលៃ;
}
