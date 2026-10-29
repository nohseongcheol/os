#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·외부 코드와 연결할 때만 사용한다. */
#define AF_INET 2
#define SOCK_STREAM 1
#define SOCK_DGRAM 2
#define IPPROTO_UDP 17
#define IPPROTO_TCP 6
#define INADDR_LOOPBACK 0x7f000001u
typedef uint32_t pk_socklen_t;
struct pk_sockaddr { uint16_t sa_family; unsigned char sa_data[14]; };
struct pk_in_addr { uint32_t s_addr; };
struct pk_sockaddr_in { uint16_t sin_family, sin_port; struct pk_in_addr sin_addr; unsigned char sin_zero[8]; };

/* 한국어 자료형은 ມາກໂຄຣ_ຄ່າ 별칭이 아닌 독립된 구조체다.
 * ອີເມວ(住所)는 도착할 곳, 갈래는 ອີເມວ ລະບົບປະຕິບັດການ_ຄ່າ, 전문(電文)은 경계 있는 통신 자료다. */
enum ເຄືອຂ່າຍ_ຄ່າຄົງທີ່ {
    ຄລາວ_ຄອບຄົວ = 2, ສະຕຣີມ_ເຄືອຂ່າຍ = 1, 전문통신 = 2,
    흐름전송규약 = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t ອີເມວ_ຄອບຄົວ; unsigned char ອີເມວ_ຂໍ້ມູນ[14]; };
struct ທີ່ຢູ່ອິນເຕີເນັດ_ຄ່າ { uint32_t ອີເມວ_ຄ່າ; };
struct 인터넷통신주소 {
    uint16_t ອີເມວ_ຄອບຄົວ;
    uint16_t ຫມາຍເລກພອດ;
    struct ທີ່ຢູ່ອິນເຕີເນັດ_ຄ່າ ທີ່ຢູ່ອິນເຕີເນັດ;
    unsigned char ຂອບເຈັຍ_ຄ່າ[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,ທີ່ຢູ່ອິນເຕີເນັດ)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 통신종단점만들기(int ອີເມວ_ຄອບຄົວ, int 통신방식, int ໂອນ_ຫຼັກການ);
int ຜູກ_ມັດ_ອີເມວ(int 종단, const struct 통신주소 *ອີເມວ, 통신주소길이형 ຄວາມຍາວ_ຄ່າ);
intptr_t 자료전문보내기(int 종단, const void *ຂໍ້ມູນ, size_t 개수, int ການ_ເລືອກ_ຄ່າ, const struct 통신주소 *ອີເມວ, 통신주소길이형 ຄວາມຍາວ_ຄ່າ);
intptr_t 자료전문받기(int 종단, void *ຂໍ້ມູນ, size_t 개수, int ການ_ເລືອກ_ຄ່າ, struct 통신주소 *ອີເມວ, 통신주소길이형 *ຄວາມຍາວ_ຄ່າ);
int 통신주소읽기(int 종단, struct 통신주소 *ອີເມວ, 통신주소길이형 *ຄວາມຍາວ_ຄ່າ);
int ເຊື່ອມຕໍ່_ເຄືອຂ່າຍ(int 종단, const struct 통신주소 *ອີເມວ, 통신주소길이형 ຄວາມຍາວ_ຄ່າ);
int 통신연결기다리기(int 종단, int 대기수);
int ຕອບຮັບ_ການ_ເຊື່ອມ_ຕໍ່_ເຄືອ_ຂ່າຍ(int 종단, struct 통신주소 *ອີເມວ, 통신주소길이형 *ຄວາມຍາວ_ຄ່າ);

int pk_connect(int fd, const struct pk_sockaddr *address, pk_socklen_t length);
int pk_listen(int fd, int backlog);
int pk_accept(int fd, struct pk_sockaddr *address, pk_socklen_t *length);
int pk_socket(int domain, int type, int protocol);
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length);
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length);
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length);
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length);
#ifdef __cplusplus
}
#endif
static inline uint16_t 망차례짧은수(uint16_t ຄ່າ) { return (uint16_t)((ຄ່າ >> 8) | (ຄ່າ << 8)); }
static inline uint32_t ເຄືອຂ່າຍ_ຕົວເລກຈໍານວນເຕັມ(uint32_t ຄ່າ) { return ((ຄ່າ & 255u) << 24) | ((ຄ່າ & 0xff00u) << 8) | ((ຄ່າ >> 8) & 0xff00u) | (ຄ່າ >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t ຄ່າ) { return 망차례짧은수(ຄ່າ); }
static inline uint32_t ມືຖື_ລໍາດັບ_ຕົວເລກຈໍານວນເຕັມ(uint32_t ຄ່າ) { return ເຄືອຂ່າຍ_ຕົວເລກຈໍານວນເຕັມ(ຄ່າ); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return ເຄືອຂ່າຍ_ຕົວເລກຈໍານວນເຕັມ(x); }
#endif
