#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·zunanji_VALUE 코드와 연결할 때만 사용한다. */
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

/* slovenščina 자료형은 makro_VALUE 별칭이 아닌 독립된 구조체다.
 * naslov(住所)는 도착할 곳, 갈래는 naslov operacijski_sistem_VALUE, datagram(電文)은 경계 있는 통신 자료다. */
enum mreža_konstanta {
    oblak_Družina = 2, tok_mreža = 1, vtičnica_za_prenos_datagramov = 2,
    tok_protokol_prenosa = 6, datagram_protokol = 17,
    naslov_povratne_zanke = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct vtičnica_naslov { uint16_t naslov_Družina; unsigned char naslov_podatki[14]; };
struct internetni_račun_VALUE { uint32_t naslov_VALUE; };
struct oblak_vtičnica_naslov {
    uint16_t naslov_Družina;
    uint16_t številka_vrat;
    struct internetni_račun_VALUE internetni_račun;
    unsigned char rob_VALUE[8];
};
typedef struct vtičnica_naslov vtičnica_naslov_Tip;
typedef struct oblak_vtičnica_naslov oblak_vtičnica_naslov_Tip;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char preveriti_oblak_vtičnica_naslov_spremeniti_velikost[(sizeof(struct oblak_vtičnica_naslov)==16)?1:-1];
typedef char preveriti_oblak_vtičnica_naslov_Krmarjenje[(offsetof(struct oblak_vtičnica_naslov,internetni_račun)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Ustvari_končna_točka(int naslov_Družina, int 통신방식, int Prenos_protokol);
int BIND_naslov(int končna_točka, const struct vtičnica_naslov *naslov, 통신주소길이형 길이);
intptr_t poslati_datagram_podatki(int končna_točka, const void *podatki, size_t element_COUNT, int izbor_VALUE, const struct vtičnica_naslov *naslov, 통신주소길이형 길이);
intptr_t sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(int končna_točka, void *podatki, size_t element_COUNT, int izbor_VALUE, struct vtičnica_naslov *naslov, 통신주소길이형 *길이);
int 통신주소읽기(int končna_točka, struct vtičnica_naslov *naslov, 통신주소길이형 *길이);
int POVEŽI_mreža(int končna_točka, const struct vtičnica_naslov *naslov, 통신주소길이형 길이);
int 통신연결기다리기(int končna_točka, int Čakanje_COUNT);
int sprejeti_omrežna_povezava(int končna_točka, struct vtičnica_naslov *naslov, 통신주소길이형 *길이);

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
static inline uint32_t mreža_celo_število(uint32_t VALUE) { return ((VALUE & 255u) << 24) | ((VALUE & 0xff00u) << 8) | ((VALUE >> 8) & 0xff00u) | (VALUE >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t VALUE) { return 망차례짧은수(VALUE); }
static inline uint32_t naprava_naročilo_celo_število(uint32_t VALUE) { return mreža_celo_število(VALUE); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return mreža_celo_število(x); }
#endif
