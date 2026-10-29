#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *नामो, socklen_t नामो_लांबाय) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)नामो, नामो_लांबाय, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *डेटा, size_t बायट_COUNT, int मांडावळी,
               const struct sockaddr *नामो, socklen_t नामो_लांबाय) {
    int 요청[2] = {(int)नामो, नामो_लांबाय};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)डेटा, बायट_COUNT, मांडावळी, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *डेटा, size_t बायट_COUNT, int मांडावळी,
                 struct sockaddr *नामो, socklen_t *नामो_लांबाय) {
    int 요청[2] = {(int)नामो, (int)नामो_लांबाय};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)डेटा, बायट_COUNT, मांडावळी, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *नामो, socklen_t *नामो_लांबाय) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)नामो, (int)नामो_लांबाय, 0, 0));
}
int setsockopt(int 파일서술자, int थर_मोल, int मांडावळी_नांव, const void *मोल, socklen_t मोल_लांबाय) {
    if (थर_मोल != SOL_SOCKET || मांडावळी_नांव != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!मोल) { errno = EFAULT; return -1; }
    if (मोल_लांबाय != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *TIME_मोल = मोल;
    if (TIME_मोल->tv_sec < 0 || TIME_मोल->tv_sec > 2 || TIME_मोल->tv_usec < 0 || TIME_मोल->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = TIME_मोल->tv_sec * 1000 + (TIME_मोल->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t मोल) { return (मोल << 8) | (मोल >> 8); }
uint16_t ntohs(uint16_t मोल) { return htons(मोल); }
uint32_t htonl(uint32_t मोल) {
    return (मोल << 24) | ((मोल << 8) & 0xff0000U) | ((मोल >> 8) & 0xff00U) | (मोल >> 24);
}
uint32_t ntohl(uint32_t मोल) { return htonl(मोल); }
int inet_pton(int 주소체계, const char *स्ट्रिंग_मोल, void *नामो) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!स्ट्रिंग_मोल || !नामो) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < 4; स्लॉट_प्रवेश++) {
        int मोल = 0, 자릿수 = 0;
        const char *चलोवप = स्ट्रिंग_मोल;
        while (*स्ट्रिंग_मोल >= '0' && *स्ट्रिंग_मोल <= '9') {
            if (++자릿수 > 3) return 0;
            मोल = मोल * 10 + *स्ट्रिंग_मोल++ - '0';
        }
        if (!자릿수 || मोल > 255 || (자릿수 > 1 && *चलोवप == '0')) return 0;
        임시[स्लॉट_प्रवेश] = मोल;
        if (स्लॉट_प्रवेश < 3) { if (*स्ट्रिंग_मोल++ != '.') return 0; }
        else if (*स्ट्रिंग_मोल) return 0;
    }
    for (int स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < 4; स्लॉट_प्रवेश++) ((unsigned char *)नामो)[स्लॉट_प्रवेश] = 임시[स्लॉट_प्रवेश];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *नामो, char *स्ट्रिंग_मोल, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!नामो || !स्ट्रिंग_मोल) { errno = EFAULT; return 0; }
    const unsigned char *수 = नामो;
    char 임시[16]; unsigned int लांबाय_मोल = 0;
    for (int स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < 4; स्लॉट_प्रवेश++) {
        unsigned int मोल = 수[स्लॉट_प्रवेश];
        if (मोल >= 100) 임시[लांबाय_मोल++] = '0' + मोल / 100;
        if (मोल >= 10) 임시[लांबाय_मोल++] = '0' + मोल / 10 % 10;
        임시[लांबाय_मोल++] = '0' + मोल % 10;
        if (स्लॉट_प्रवेश < 3) 임시[लांबाय_मोल++] = '.';
    }
    임시[लांबाय_मोल++] = 0;
    if (용량 < लांबाय_मोल) { errno = ENOSPC; return 0; }
    for (unsigned int स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < लांबाय_मोल; स्लॉट_प्रवेश++) स्ट्रिंग_मोल[स्लॉट_प्रवेश] = 임시[स्लॉट_प्रवेश];
    return स्ट्रिंग_मोल;
}
