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

/* 한국어 자료형은 makros_baha 별칭이 아닌 독립된 구조체다.
 * salgy(住所)는 도착할 곳, 갈래는 salgy operasiýa_ulgamy_baha, 전문(電文)은 경계 있는 통신 자료다. */
enum Tor_hemişelik {
    bulut_Maşgala = 2, Stream_Tor = 1, 전문통신 = 2,
    흐름전송규약 = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t salgy_Maşgala; unsigned char salgy_maglumat[14]; };
struct Internet_salgy_baha { uint32_t salgy_baha; };
struct 인터넷통신주소 {
    uint16_t salgy_Maşgala;
    uint16_t 접속번호;
    struct Internet_salgy_baha Internet_salgy;
    unsigned char araçäk_baha[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,Internet_salgy)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int 통신종단점만들기(int salgy_Maşgala, int 통신방식, int geçir_protokol);
int BIND_salgy(int 종단, const struct 통신주소 *salgy, 통신주소길이형 dowamlylyk_baha);
intptr_t 자료전문보내기(int 종단, const void *maglumat, size_t 개수, int saýlama_baha, const struct 통신주소 *salgy, 통신주소길이형 dowamlylyk_baha);
intptr_t 자료전문받기(int 종단, void *maglumat, size_t 개수, int saýlama_baha, struct 통신주소 *salgy, 통신주소길이형 *dowamlylyk_baha);
int 통신주소읽기(int 종단, struct 통신주소 *salgy, 통신주소길이형 *dowamlylyk_baha);
int Birikme_Tor(int 종단, const struct 통신주소 *salgy, 통신주소길이형 dowamlylyk_baha);
int 통신연결기다리기(int 종단, int 대기수);
int kabul_et_tor_birikmesi(int 종단, struct 통신주소 *salgy, 통신주소길이형 *dowamlylyk_baha);

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
static inline uint16_t 망차례짧은수(uint16_t baha) { return (uint16_t)((baha >> 8) | (baha << 8)); }
static inline uint32_t Tor_bitin(uint32_t baha) { return ((baha & 255u) << 24) | ((baha & 0xff00u) << 8) | ((baha >> 8) & 0xff00u) | (baha >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t baha) { return 망차례짧은수(baha); }
static inline uint32_t enjam_tertip_bitin(uint32_t baha) { return Tor_bitin(baha); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return Tor_bitin(x); }
#endif
