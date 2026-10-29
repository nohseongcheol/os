#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·vanjski_VALUE 코드와 연결할 때만 사용한다. */
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

/* hrvatski 자료형은 makro_VALUE 별칭이 아닌 독립된 구조체다.
 * adresa(住所)는 도착할 곳, 갈래는 adresa operacijski_sustav_VALUE, datogram(電文)은 경계 있는 통신 자료다. */
enum mreža_konstanta {
    oblak_linija = 2, tok_mreža = 1, datogramska_utičnica = 2,
    tok_protokol_za_prijenos = 6, datogram_protokol = 17,
    povratna_adresa = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t adresa_linija; unsigned char adresa_podaci[14]; };
struct internetska_adresa_VALUE { uint32_t adresa_VALUE; };
struct 인터넷통신주소 {
    uint16_t adresa_linija;
    uint16_t broj_priključka;
    struct internetska_adresa_VALUE internetska_adresa;
    unsigned char margina_VALUE[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,internetska_adresa)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Create_sudionik(int adresa_linija, int 통신방식, int Prijenos_protokol);
int BIND_adresa(int sudionik, const struct 통신주소 *adresa, 통신주소길이형 길이);
intptr_t slati_datogram_podaci(int sudionik, const void *podaci, size_t artikl_COUNT, int odabir_VALUE, const struct 통신주소 *adresa, 통신주소길이형 길이);
intptr_t primiti_datogram_podaci(int sudionik, void *podaci, size_t artikl_COUNT, int odabir_VALUE, struct 통신주소 *adresa, 통신주소길이형 *길이);
int 통신주소읽기(int sudionik, struct 통신주소 *adresa, 통신주소길이형 *길이);
int CONNECT_mreža(int sudionik, const struct 통신주소 *adresa, 통신주소길이형 길이);
int 통신연결기다리기(int sudionik, int Čekanje_COUNT);
int prihvatiti_mrežna_veza(int sudionik, struct 통신주소 *adresa, 통신주소길이형 *길이);

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
static inline uint16_t 망차례짧은수(uint16_t VALUE) { return (uint16_t)((VALUE >> 8) | (VALUE << 8)); }
static inline uint32_t mreža_cijeli_broj(uint32_t VALUE) { return ((VALUE & 255u) << 24) | ((VALUE & 0xff00u) << 8) | ((VALUE >> 8) & 0xff00u) | (VALUE >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t VALUE) { return 망차례짧은수(VALUE); }
static inline uint32_t uređaj_narudžba_cijeli_broj(uint32_t VALUE) { return mreža_cijeli_broj(VALUE); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return mreža_cijeli_broj(x); }
#endif
