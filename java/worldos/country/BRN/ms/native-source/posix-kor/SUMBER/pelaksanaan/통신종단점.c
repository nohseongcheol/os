#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *e_mel, socklen_t e_mel_kepanjangan) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)e_mel, e_mel_kepanjangan, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t bait_COUNT, int Tetapan,
               const struct sockaddr *e_mel, socklen_t e_mel_kepanjangan) {
    int permintaan[2] = {(int)e_mel, e_mel_kepanjangan};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, bait_COUNT, Tetapan, (int)permintaan));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t bait_COUNT, int Tetapan,
                 struct sockaddr *e_mel, socklen_t *e_mel_kepanjangan) {
    int permintaan[2] = {(int)e_mel, (int)e_mel_kepanjangan};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, bait_COUNT, Tetapan, (int)permintaan));
}
int getsockname(int 파일서술자, struct sockaddr *e_mel, socklen_t *e_mel_kepanjangan) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)e_mel, (int)e_mel_kepanjangan, 0, 0));
}
int setsockopt(int 파일서술자, int lapisan_VALUE, int Seting_nama, const void *VALUE, socklen_t VALUE_kepanjangan) {
    if (lapisan_VALUE != SOL_SOCKET || Seting_nama != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_kepanjangan != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *nilai_masa = VALUE;
    if (nilai_masa->tv_sec < 0 || nilai_masa->tv_sec > 2 || nilai_masa->tv_usec < 0 || nilai_masa->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = nilai_masa->tv_sec * 1000 + (nilai_masa->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VALUE) { return (VALUE << 8) | (VALUE >> 8); }
uint16_t ntohs(uint16_t VALUE) { return htons(VALUE); }
uint32_t htonl(uint32_t VALUE) {
    return (VALUE << 24) | ((VALUE << 8) & 0xff0000U) | ((VALUE >> 8) & 0xff00U) | (VALUE >> 24);
}
uint32_t ntohl(uint32_t VALUE) { return htonl(VALUE); }
int inet_pton(int 주소체계, const char *rentetan_VALUE, void *e_mel) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!rentetan_VALUE || !e_mel) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int 칸 = 0; 칸 < 4; 칸++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Jalan = rentetan_VALUE;
        while (*rentetan_VALUE >= '0' && *rentetan_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *rentetan_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Jalan == '0')) return 0;
        임시[칸] = VALUE;
        if (칸 < 3) { if (*rentetan_VALUE++ != '.') return 0; }
        else if (*rentetan_VALUE) return 0;
    }
    for (int 칸 = 0; 칸 < 4; 칸++) ((unsigned char *)e_mel)[칸] = 임시[칸];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *e_mel, char *rentetan_VALUE, socklen_t kapasiti_VALUE) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!e_mel || !rentetan_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = e_mel;
    char 임시[16]; unsigned int kepanjangan_VALUE = 0;
    for (int 칸 = 0; 칸 < 4; 칸++) {
        unsigned int VALUE = 수[칸];
        if (VALUE >= 100) 임시[kepanjangan_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[kepanjangan_VALUE++] = '0' + VALUE / 10 % 10;
        임시[kepanjangan_VALUE++] = '0' + VALUE % 10;
        if (칸 < 3) 임시[kepanjangan_VALUE++] = '.';
    }
    임시[kepanjangan_VALUE++] = 0;
    if (kapasiti_VALUE < kepanjangan_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int 칸 = 0; 칸 < kepanjangan_VALUE; 칸++) rentetan_VALUE[칸] = 임시[칸];
    return rentetan_VALUE;
}
