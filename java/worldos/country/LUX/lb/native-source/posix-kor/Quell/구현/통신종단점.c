#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *Adress, socklen_t Adress_Längt) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)Adress, Adress_Längt, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *Daten, size_t Byte_COUNT, int Astellungen,
               const struct sockaddr *Adress, socklen_t Adress_Längt) {
    int 요청[2] = {(int)Adress, Adress_Längt};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)Daten, Byte_COUNT, Astellungen, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *Daten, size_t Byte_COUNT, int Astellungen,
                 struct sockaddr *Adress, socklen_t *Adress_Längt) {
    int 요청[2] = {(int)Adress, (int)Adress_Längt};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)Daten, Byte_COUNT, Astellungen, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *Adress, socklen_t *Adress_Längt) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)Adress, (int)Adress_Längt, 0, 0));
}
int setsockopt(int 파일서술자, int Layer_VALUE, int Astellungen_Numm, const void *VALUE, socklen_t VALUE_Längt) {
    if (Layer_VALUE != SOL_SOCKET || Astellungen_Numm != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!VALUE) { errno = EFAULT; return -1; }
    if (VALUE_Längt != sizeof(struct timeval)) { errno = EINVAL; return -1; }
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
int inet_pton(int 주소체계, const char *Zeechefolleg_VALUE, void *Adress) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!Zeechefolleg_VALUE || !Adress) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int Slot_Agab = 0; Slot_Agab < 4; Slot_Agab++) {
        int VALUE = 0, 자릿수 = 0;
        const char *Laf = Zeechefolleg_VALUE;
        while (*Zeechefolleg_VALUE >= '0' && *Zeechefolleg_VALUE <= '9') {
            if (++자릿수 > 3) return 0;
            VALUE = VALUE * 10 + *Zeechefolleg_VALUE++ - '0';
        }
        if (!자릿수 || VALUE > 255 || (자릿수 > 1 && *Laf == '0')) return 0;
        임시[Slot_Agab] = VALUE;
        if (Slot_Agab < 3) { if (*Zeechefolleg_VALUE++ != '.') return 0; }
        else if (*Zeechefolleg_VALUE) return 0;
    }
    for (int Slot_Agab = 0; Slot_Agab < 4; Slot_Agab++) ((unsigned char *)Adress)[Slot_Agab] = 임시[Slot_Agab];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *Adress, char *Zeechefolleg_VALUE, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!Adress || !Zeechefolleg_VALUE) { errno = EFAULT; return 0; }
    const unsigned char *수 = Adress;
    char 임시[16]; unsigned int Längt_VALUE = 0;
    for (int Slot_Agab = 0; Slot_Agab < 4; Slot_Agab++) {
        unsigned int VALUE = 수[Slot_Agab];
        if (VALUE >= 100) 임시[Längt_VALUE++] = '0' + VALUE / 100;
        if (VALUE >= 10) 임시[Längt_VALUE++] = '0' + VALUE / 10 % 10;
        임시[Längt_VALUE++] = '0' + VALUE % 10;
        if (Slot_Agab < 3) 임시[Längt_VALUE++] = '.';
    }
    임시[Längt_VALUE++] = 0;
    if (용량 < Längt_VALUE) { errno = ENOSPC; return 0; }
    for (unsigned int Slot_Agab = 0; Slot_Agab < Längt_VALUE; Slot_Agab++) Zeechefolleg_VALUE[Slot_Agab] = 임시[Slot_Agab];
    return Zeechefolleg_VALUE;
}
