#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·външен_стойност 코드와 연결할 때만 사용한다. */
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

/* Български 자료형은 макрос_стойност 별칭이 아닌 독립된 구조체다.
 * адрес(住所)는 도착할 곳, 갈래는 адрес операционна_система_стойност, дейтаграма(電文)은 경계 있는 통신 자료다. */
enum мрежа_константа {
    облак_семейни = 2, поток_мрежа = 1, дейтаграмно_гнездо = 2,
    поток_транспортен_протокол = 6, дейтаграма_протокол = 17,
    адрес_за_обръщане_към_себе_си = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t адрес_семейни; unsigned char адрес_данни[14]; };
struct Интернет_адрес_стойност { uint32_t адрес_стойност; };
struct 인터넷통신주소 {
    uint16_t адрес_семейни;
    uint16_t номер_на_порт;
    struct Интернет_адрес_стойност Интернет_адрес;
    unsigned char поле_стойност[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,Интернет_адрес)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Създаване_участник(int адрес_семейни, int 통신방식, int прехвърлям_протокол);
int обвързвам_адрес(int участник, const struct 통신주소 *адрес, 통신주소길이형 길이);
intptr_t изпращам_дейтаграма_данни(int участник, const void *данни, size_t 개수, int избор_стойност, const struct 통신주소 *адрес, 통신주소길이형 길이);
intptr_t получавам_дейтаграма_данни(int участник, void *данни, size_t 개수, int избор_стойност, struct 통신주소 *адрес, 통신주소길이형 *길이);
int 통신주소읽기(int участник, struct 통신주소 *адрес, 통신주소길이형 *길이);
int връзка_мрежа(int участник, const struct 통신주소 *адрес, 통신주소길이형 길이);
int 통신연결기다리기(int участник, int 대기수);
int приемам_мрежова_връзка(int участник, struct 통신주소 *адрес, 통신주소길이형 *길이);

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
static inline uint16_t 망차례짧은수(uint16_t стойност) { return (uint16_t)((стойност >> 8) | (стойност << 8)); }
static inline uint32_t мрежа_цяло_число(uint32_t стойност) { return ((стойност & 255u) << 24) | ((стойност & 0xff00u) << 8) | ((стойност >> 8) & 0xff00u) | (стойност >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t стойност) { return 망차례짧은수(стойност); }
static inline uint32_t устройство_ред_цяло_число(uint32_t стойност) { return мрежа_цяло_число(стойност); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return мрежа_цяло_число(x); }
#endif
