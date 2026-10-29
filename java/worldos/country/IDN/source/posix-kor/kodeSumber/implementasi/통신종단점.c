#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *surel, socklen_t surel_panjang) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)surel, surel_panjang, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *data, size_t byte_COUNT, int Konfigurasi,
               const struct sockaddr *surel, socklen_t surel_panjang) {
    int permintaan[2] = {(int)surel, surel_panjang};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)data, byte_COUNT, Konfigurasi, (int)permintaan));
}
ssize_t recvfrom(int 파일서술자, void *data, size_t byte_COUNT, int Konfigurasi,
                 struct sockaddr *surel, socklen_t *surel_panjang) {
    int permintaan[2] = {(int)surel, (int)surel_panjang};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)data, byte_COUNT, Konfigurasi, (int)permintaan));
}
int getsockname(int 파일서술자, struct sockaddr *surel, socklen_t *surel_panjang) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)surel, (int)surel_panjang, 0, 0));
}
int setsockopt(int 파일서술자, int lapisan_VALUE, int Pengaturan_nama, const void *VALUE, socklen_t VALUE_panjang) {
    if (lapisan_VALUE != SOL_SOCKET || Pengaturan_nama != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_panjang != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *TIME_VALUE = VALUE;
    if (TIME_VALUE->tv_sec < 0 || TIME_VALUE->tv_sec > 2 || TIME_VALUE->tv_usec < 0 || TIME_VALUE->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = TIME_VALUE->tv_sec * 1000 + (TIME_VALUE->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t VALUE) { return (VALUE << 8) | (VALUE >> 8); }
uint16_t ntohs(uint16_t VALUE) { return htons(VALUE); }
uint32_t htonl(uint32_t VALUE) {
    return (VALUE << 24) | ((VALUE << 8) & 0xff0000U) | ((VALUE >> 8) & 0xff00U) | (VALUE >> 24);
}
uint32_t ntohl(uint32_t VALUE) { return htonl(VALUE); }
int inet_pton(int 주소체계, const char *string_VALUE, void *surel) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!string_VALUE || !surel) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int slot_entri = 0; slot_entri < 4; slot_entri++) {
        int VALUE = 0, 자릿수 = 0;
        const char *jalankan = string_VALUE;
        while (*string_VALUE >= '0' && *string_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *string_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *jalankan == '0')) return 0;
        임시[slot_entri] = VALUE;
        if (slot_entri < 3) { if (*string_VALUE++ != '.') return 0; }
        else if (*string_VALUE) return 0;
    }
    for (int slot_entri = 0; slot_entri < 4; slot_entri++) ((unsigned char *)surel)[slot_entri] = 임시[slot_entri];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *surel, char *string_VALUE, socklen_t kapasitas_VALUE) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!surel || !string_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = surel;
    char 임시[16]; unsigned int panjang_VALUE = 0;
    for (int slot_entri = 0; slot_entri < 4; slot_entri++) {
        unsigned int VALUE = 수[slot_entri];
        if (VALUE >= 100) 임시[panjang_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[panjang_VALUE++] = '0' + VALUE / 10 % 10;
        임시[panjang_VALUE++] = '0' + VALUE % 10;
        if (slot_entri < 3) 임시[panjang_VALUE++] = '.';
    }
    임시[panjang_VALUE++] = 0;
    if (kapasitas_VALUE < panjang_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int slot_entri = 0; slot_entri < panjang_VALUE; slot_entri++) string_VALUE[slot_entri] = 임시[slot_entri];
    return string_VALUE;
}
