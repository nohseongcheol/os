#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·сыртқы_мән 코드와 연결할 때만 사용한다. */
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

/* 한국어 자료형은 макрос_мән 별칭이 아닌 독립된 구조체다.
 * мекенжай(住所)는 도착할 곳, 갈래는 мекенжай операциялық_жүйе_мән, 전문(電文)은 경계 있는 통신 자료다. */
enum желі_тұрақты_мән {
    бұлт_топ = 2, ағым_желі = 1, 전문통신 = 2,
    ағым_транспорт_протоколы = 6, 전문전송규약 = 17,
    кері_тұйықталу_мекенжайы = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t мекенжай_топ; unsigned char мекенжай_деректер[14]; };
struct Интернет_мекенжайы_мән { uint32_t мекенжай_мән; };
struct 인터넷통신주소 {
    uint16_t мекенжай_топ;
    uint16_t порт_нөмірі;
    struct Интернет_мекенжайы_мән Интернет_мекенжайы;
    unsigned char шет_мән[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,Интернет_мекенжайы)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int жасау_қатысушы(int мекенжай_топ, int 통신방식, int аудару_протокол);
int байланыстыру_мекенжай(int қатысушы, const struct 통신주소 *мекенжай, 통신주소길이형 ұзындық_мән);
intptr_t 자료전문보내기(int қатысушы, const void *деректер, size_t 개수, int таңдау_мән, const struct 통신주소 *мекенжай, 통신주소길이형 ұзындық_мән);
intptr_t 자료전문받기(int қатысушы, void *деректер, size_t 개수, int таңдау_мән, struct 통신주소 *мекенжай, 통신주소길이형 *ұзындық_мән);
int 통신주소읽기(int қатысушы, struct 통신주소 *мекенжай, 통신주소길이형 *ұзындық_мән);
int қосу_желі(int қатысушы, const struct 통신주소 *мекенжай, 통신주소길이형 ұзындық_мән);
int 통신연결기다리기(int қатысушы, int 대기수);
int қабылдау_желілік_байланыс(int қатысушы, struct 통신주소 *мекенжай, 통신주소길이형 *ұзындық_мән);

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
static inline uint16_t 망차례짧은수(uint16_t мән) { return (uint16_t)((мән >> 8) | (мән << 8)); }
static inline uint32_t желі_бүтін_сан(uint32_t мән) { return ((мән & 255u) << 24) | ((мән & 0xff00u) << 8) | ((мән >> 8) & 0xff00u) | (мән >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t мән) { return 망차례짧은수(мән); }
static inline uint32_t құрылғы_рет_бүтін_сан(uint32_t мән) { return желі_бүтін_сан(мән); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return желі_бүтін_сан(x); }
#endif
