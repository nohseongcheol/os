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

/* Reo_Māori 자료형은 tonotono_uara 별칭이 아닌 독립된 구조체다.
 * ADDRESS(住所)는 도착할 곳, 갈래는 ADDRESS pūnaha_mahi_uara, 전문(電文)은 경계 있는 통신 자료다. */
enum whatunga_taimau {
    kapua_Whānau = 2, roma_whatunga = 1, 전문통신 = 2,
    흐름전송규약 = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t ADDRESS_Whānau; unsigned char ADDRESS_raraunga[14]; };
struct Wāhitau_ipurangi_uara { uint32_t ADDRESS_uara; };
struct 인터넷통신주소 {
    uint16_t ADDRESS_Whānau;
    uint16_t 접속번호;
    struct Wāhitau_ipurangi_uara Wāhitau_ipurangi;
    unsigned char tawhē_uara[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,Wāhitau_ipurangi)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 통신종단점만들기(int ADDRESS_Whānau, int 통신방식, int whakawhiti_kawa);
int BIND_ADDRESS(int 종단, const struct 통신주소 *ADDRESS, 통신주소길이형 roa_uara);
intptr_t 자료전문보내기(int 종단, const void *raraunga, size_t tuemi_COUNT, int tīpakonga_uara, const struct 통신주소 *ADDRESS, 통신주소길이형 roa_uara);
intptr_t 자료전문받기(int 종단, void *raraunga, size_t tuemi_COUNT, int tīpakonga_uara, struct 통신주소 *ADDRESS, 통신주소길이형 *roa_uara);
int 통신주소읽기(int 종단, struct 통신주소 *ADDRESS, 통신주소길이형 *roa_uara);
int TŪHONO_whatunga(int 종단, const struct 통신주소 *ADDRESS, 통신주소길이형 roa_uara);
int 통신연결기다리기(int 종단, int 대기수);
int whakaae_tūhononga_whatunga(int 종단, struct 통신주소 *ADDRESS, 통신주소길이형 *roa_uara);

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
static inline uint16_t 망차례짧은수(uint16_t uara) { return (uint16_t)((uara >> 8) | (uara << 8)); }
static inline uint32_t whatunga_tau_tōpū(uint32_t uara) { return ((uara & 255u) << 24) | ((uara & 0xff00u) << 8) | ((uara >> 8) & 0xff00u) | (uara >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t uara) { return 망차례짧은수(uara); }
static inline uint32_t pūkoro_whakaraupapa_tau_tōpū(uint32_t uara) { return whatunga_tau_tōpū(uara); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return whatunga_tau_tōpū(x); }
#endif
