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

/* 한국어 자료형은 makro_thamani 별칭이 아닌 독립된 구조체다.
 * anwani(住所)는 도착할 곳, 갈래는 anwani mfumo_endeshi_thamani, 전문(電文)은 경계 있는 통신 자료다. */
enum Mtandao_kisobadilika {
    wingu_Familia = 2, Stream_Mtandao = 1, 전문통신 = 2,
    흐름전송규약 = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t anwani_Familia; unsigned char anwani_data[14]; };
struct Anwani_tovuti_thamani { uint32_t anwani_thamani; };
struct 인터넷통신주소 {
    uint16_t anwani_Familia;
    uint16_t namba_ya_kituo;
    struct Anwani_tovuti_thamani Anwani_tovuti;
    unsigned char pambizo_thamani[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,Anwani_tovuti)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 통신종단점만들기(int anwani_Familia, int 통신방식, int hamisha_itifaki);
int FUNGA_anwani(int 종단, const struct 통신주소 *anwani, 통신주소길이형 urefu_thamani);
intptr_t 자료전문보내기(int 종단, const void *data, size_t 개수, int uteuzi_thamani, const struct 통신주소 *anwani, 통신주소길이형 urefu_thamani);
intptr_t 자료전문받기(int 종단, void *data, size_t 개수, int uteuzi_thamani, struct 통신주소 *anwani, 통신주소길이형 *urefu_thamani);
int 통신주소읽기(int 종단, struct 통신주소 *anwani, 통신주소길이형 *urefu_thamani);
int UNGANISHA_Mtandao(int 종단, const struct 통신주소 *anwani, 통신주소길이형 urefu_thamani);
int 통신연결기다리기(int 종단, int 대기수);
int kubali_muunganisho_wa_mtandao(int 종단, struct 통신주소 *anwani, 통신주소길이형 *urefu_thamani);

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
static inline uint16_t 망차례짧은수(uint16_t thamani) { return (uint16_t)((thamani >> 8) | (thamani << 8)); }
static inline uint32_t Mtandao_namba_kamili(uint32_t thamani) { return ((thamani & 255u) << 24) | ((thamani & 0xff00u) << 8) | ((thamani >> 8) & 0xff00u) | (thamani >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t thamani) { return 망차례짧은수(thamani); }
static inline uint32_t kifaa_mpangilio_namba_kamili(uint32_t thamani) { return Mtandao_namba_kamili(thamani); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return Mtandao_namba_kamili(x); }
#endif
