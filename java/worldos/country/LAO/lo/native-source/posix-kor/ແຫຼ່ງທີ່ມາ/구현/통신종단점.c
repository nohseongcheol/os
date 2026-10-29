#include <통신규약.h>
#include <errno.h>
#include "호출경계.h"

int socket(int 주소체계, int 통신종류, int 규약번호) {
    return 호출결과(jkoros_syscall(41, 주소체계, 통신종류, 규약번호, 0, 0));
}
int bind(int 파일서술자, const struct sockaddr *ອີເມວ, socklen_t ອີເມວ_ຄວາມຍາວ) {
    return 호출결과(jkoros_syscall(42, 파일서술자, (int)ອີເມວ, ອີເມວ_ຄວາມຍາວ, 0, 0));
}
ssize_t sendto(int 파일서술자, const void *ຂໍ້ມູນ, size_t 바이트수, int ການຕັ້ງຄ່າ,
               const struct sockaddr *ອີເມວ, socklen_t ອີເມວ_ຄວາມຍາວ) {
    int 요청[2] = {(int)ອີເມວ, ອີເມວ_ຄວາມຍາວ};
    return 호출결과(jkoros_syscall(43, 파일서술자, (int)ຂໍ້ມູນ, 바이트수, ການຕັ້ງຄ່າ, (int)요청));
}
ssize_t recvfrom(int 파일서술자, void *ຂໍ້ມູນ, size_t 바이트수, int ການຕັ້ງຄ່າ,
                 struct sockaddr *ອີເມວ, socklen_t *ອີເມວ_ຄວາມຍາວ) {
    int 요청[2] = {(int)ອີເມວ, (int)ອີເມວ_ຄວາມຍາວ};
    return 호출결과(jkoros_syscall(44, 파일서술자, (int)ຂໍ້ມູນ, 바이트수, ການຕັ້ງຄ່າ, (int)요청));
}
int getsockname(int 파일서술자, struct sockaddr *ອີເມວ, socklen_t *ອີເມວ_ຄວາມຍາວ) {
    return 호출결과(jkoros_syscall(45, 파일서술자, (int)ອີເມວ, (int)ອີເມວ_ຄວາມຍາວ, 0, 0));
}
int setsockopt(int 파일서술자, int ຊັ້ນ_ຄ່າ, int ການຕັ້ງຄ່າ_ຊື່, const void *ຄ່າ, socklen_t ຄ່າ_ຄວາມຍາວ) {
    if (ຊັ້ນ_ຄ່າ != SOL_SOCKET || ການຕັ້ງຄ່າ_ຊື່ != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!ຄ່າ) { errno = EFAULT; return -1; }
    if (ຄ່າ_ຄວາມຍາວ != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *ເວລາ_ຄ່າ = ຄ່າ;
    if (ເວລາ_ຄ່າ->tv_sec < 0 || ເວລາ_ຄ່າ->tv_sec > 2 || ເວລາ_ຄ່າ->tv_usec < 0 || ເວລາ_ຄ່າ->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int 밀리초 = ເວລາ_ຄ່າ->tv_sec * 1000 + (ເວລາ_ຄ່າ->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, 파일서술자, 밀리초, 0, 0, 0));
}
uint16_t htons(uint16_t ຄ່າ) { return (ຄ່າ << 8) | (ຄ່າ >> 8); }
uint16_t ntohs(uint16_t ຄ່າ) { return htons(ຄ່າ); }
uint32_t htonl(uint32_t ຄ່າ) {
    return (ຄ່າ << 24) | ((ຄ່າ << 8) & 0xff0000U) | ((ຄ່າ >> 8) & 0xff00U) | (ຄ່າ >> 24);
}
uint32_t ntohl(uint32_t ຄ່າ) { return htonl(ຄ່າ); }
int inet_pton(int 주소체계, const char *ສະຕຣິງ_ຄ່າ, void *ອີເມວ) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!ສະຕຣິງ_ຄ່າ || !ອີເມວ) { errno = EFAULT; return -1; }
    unsigned char 임시[4];
    for (int ຊ່ອງ_ເຂົ້າໃນ = 0; ຊ່ອງ_ເຂົ້າໃນ < 4; ຊ່ອງ_ເຂົ້າໃນ++) {
        int ຄ່າ = 0, 자릿수 = 0;
        const char *ແລ່ນ = ສະຕຣິງ_ຄ່າ;
        while (*ສະຕຣິງ_ຄ່າ >= '0' && *ສະຕຣິງ_ຄ່າ <= '9') {
            if (++자릿수 > 3) return 0;
            ຄ່າ = ຄ່າ * 10 + *ສະຕຣິງ_ຄ່າ++ - '0';
        }
        if (!자릿수 || ຄ່າ > 255 || (자릿수 > 1 && *ແລ່ນ == '0')) return 0;
        임시[ຊ່ອງ_ເຂົ້າໃນ] = ຄ່າ;
        if (ຊ່ອງ_ເຂົ້າໃນ < 3) { if (*ສະຕຣິງ_ຄ່າ++ != '.') return 0; }
        else if (*ສະຕຣິງ_ຄ່າ) return 0;
    }
    for (int ຊ່ອງ_ເຂົ້າໃນ = 0; ຊ່ອງ_ເຂົ້າໃນ < 4; ຊ່ອງ_ເຂົ້າໃນ++) ((unsigned char *)ອີເມວ)[ຊ່ອງ_ເຂົ້າໃນ] = 임시[ຊ່ອງ_ເຂົ້າໃນ];
    return 1;
}
const char *inet_ntop(int 주소체계, const void *ອີເມວ, char *ສະຕຣິງ_ຄ່າ, socklen_t 용량) {
    if (주소체계 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!ອີເມວ || !ສະຕຣິງ_ຄ່າ) { errno = EFAULT; return 0; }
    const unsigned char *수 = ອີເມວ;
    char 임시[16]; unsigned int ຄວາມຍາວ_ຄ່າ = 0;
    for (int ຊ່ອງ_ເຂົ້າໃນ = 0; ຊ່ອງ_ເຂົ້າໃນ < 4; ຊ່ອງ_ເຂົ້າໃນ++) {
        unsigned int ຄ່າ = 수[ຊ່ອງ_ເຂົ້າໃນ];
        if (ຄ່າ >= 100) 임시[ຄວາມຍາວ_ຄ່າ++] = '0' + ຄ່າ / 100;
        if (ຄ່າ >= 10) 임시[ຄວາມຍາວ_ຄ່າ++] = '0' + ຄ່າ / 10 % 10;
        임시[ຄວາມຍາວ_ຄ່າ++] = '0' + ຄ່າ % 10;
        if (ຊ່ອງ_ເຂົ້າໃນ < 3) 임시[ຄວາມຍາວ_ຄ່າ++] = '.';
    }
    임시[ຄວາມຍາວ_ຄ່າ++] = 0;
    if (용량 < ຄວາມຍາວ_ຄ່າ) { errno = ENOSPC; return 0; }
    for (unsigned int ຊ່ອງ_ເຂົ້າໃນ = 0; ຊ່ອງ_ເຂົ້າໃນ < ຄວາມຍາວ_ຄ່າ; ຊ່ອງ_ເຂົ້າໃນ++) ສະຕຣິງ_ຄ່າ[ຊ່ອງ_ເຂົ້າໃນ] = 임시[ຊ່ອງ_ເຂົ້າໃນ];
    return ສະຕຣິງ_ຄ່າ;
}
