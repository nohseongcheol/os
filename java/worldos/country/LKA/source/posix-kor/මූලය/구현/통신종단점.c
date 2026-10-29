#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *යොමුව, socklen_t යොමුව_දිග) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)යොමුව, යොමුව_දිග, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *දත්ත, size_t 바이트수, int සැකසුම්,
               const struct sockaddr *යොමුව, socklen_t යොමුව_දිග) {
    int 요청[2] = {(int)යොමුව, යොමුව_දිග};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)දත්ත, 바이트수, සැකසුම්, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *දත්ත, size_t 바이트수, int සැකසුම්,
                 struct sockaddr *යොමුව, socklen_t *යොමුව_දිග) {
    int 요청[2] = {(int)යොමුව, (int)යොමුව_දිග};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)දත්ත, 바이트수, සැකසුම්, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *යොමුව, socklen_t *යොමුව_දිග) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)යොමුව, (int)යොමුව_දිග, 0, 0));
}
int setsockopt(int 파일서술자, int ස්තරය_අගය, int පසුතල_නම, const void *අගය, socklen_t අගය_දිග) {
    if (ස්තරය_අගය != SOL_SOCKET || පසුතල_නම != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!අගය) { errno = EFAULT; return -1; }
    if (අගය_දිග != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *시간 = අගය;
    if (시간->tv_sec < 0 || 시간->tv_sec > 2 || 시간->tv_usec < 0 || 시간->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = 시간->tv_sec * 1000 + (시간->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t අගය) { return (අගය << 8) | (අගය >> 8); }
uint16_t ntohs(uint16_t අගය) { return htons(අගය); }
uint32_t htonl(uint32_t අගය) {
    return (අගය << 24) | ((අගය << 8) & 0xff0000U) | ((අගය >> 8) & 0xff00U) | (අගය >> 24);
}
uint32_t ntohl(uint32_t අගය) { return htonl(අගය); }
int inet_pton(int 주소체계, const char *අනුලකුණු_වැල_අගය, void *යොමුව) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!අනුලකුණු_වැල_අගය || !යොමුව) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int විවරය_පිවිසුම = 0; විවරය_පිවිසුම < 4; විවරය_පිවිසුම++) {
        int අගය = 0, 자릿수 = 0;
        const char *ක්_රියාත්මක_කරන්න_2 = අනුලකුණු_වැල_අගය;
        while (*අනුලකුණු_වැල_අගය >= '0' && *අනුලකුණු_වැල_අගය <= '9') {
            if (++자릿수 > 3) return 0;
            අගය = අගය * 10 + *අනුලකුණු_වැල_අගය++ - '0';
        }
        if (!자릿수 || අගය > 255 || (자릿수 > 1 && *ක්_රියාත්මක_කරන්න_2 == '0')) return 0;
        임시[විවරය_පිවිසුම] = අගය;
        if (විවරය_පිවිසුම < 3) { if (*අනුලකුණු_වැල_අගය++ != '.') return 0; }
        else if (*අනුලකුණු_වැල_අගය) return 0;
    }
    for (int විවරය_පිවිසුම = 0; විවරය_පිවිසුම < 4; විවරය_පිවිසුම++) ((unsigned char *)යොමුව)[විවරය_පිවිසුම] = 임시[විවරය_පිවිසුම];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *යොමුව, char *අනුලකුණු_වැල_අගය, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!යොමුව || !අනුලකුණු_වැල_අගය) { errno = EFAULT; return 0; }
    const unsigned char *수 = යොමුව;
    char 임시[16]; unsigned int දිග_අගය = 0;
    for (int විවරය_පිවිසුම = 0; විවරය_පිවිසුම < 4; විවරය_පිවිසුම++) {
        unsigned int අගය = 수[විවරය_පිවිසුම];
        if (අගය >= 100) 임시[දිග_අගය++] = '0' + අගය / 100;
        if (අගය >= 10) 임시[දිග_අගය++] = '0' + අගය / 10 % 10;
        임시[දිග_අගය++] = '0' + අගය % 10;
        if (විවරය_පිවිසුම < 3) 임시[දිග_අගය++] = '.';
    }
    임시[දිග_අගය++] = 0;
    if (용량 < දිග_අගය) { errno = ENOSPC; return 0; }
    for (unsigned int විවරය_පිවිසුම = 0; විවරය_පිවිසුම < දිග_අගය; විවරය_පිවිසුම++) අනුලකුණු_වැල_අගය[විවරය_පිවිසුම] = 임시[විවරය_පිවිසුම];
    return අනුලකුණු_වැල_අගය;
}
