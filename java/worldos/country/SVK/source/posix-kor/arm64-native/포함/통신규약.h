#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 spustiteľný_súbor·externý_VALUE 코드와 연결할 때만 사용한다. */
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

/* Slovenský 자료형은 makro_VALUE 별칭이 아닌 독립된 구조체다.
 * adresa(住所)는 도착할 곳, 갈래는 adresa operačný_systém_VALUE, datagram(電文)은 경계 있는 통신 자료다. */
enum sieť_konštanta {
    cloud_séria = 2, Stream_sieť = 1, datagramový_soket = 2,
    Stream_prenosový_protokol = 6, datagram_protokol = 17,
    adresa_systémovej_slučky = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t soket_adresa_dĺžka_Typ;
struct soket_adresa { uint16_t adresa_séria; unsigned char adresa_údaje[14]; };
struct internetová_adresa_VALUE { uint32_t adresa_VALUE; };
struct cloud_soket_adresa {
    uint16_t adresa_séria;
    uint16_t číslo_portu;
    struct internetová_adresa_VALUE internetová_adresa;
    unsigned char okraj_VALUE[8];
};
typedef struct soket_adresa soket_adresa_Typ;
typedef struct cloud_soket_adresa cloud_soket_adresa_Typ;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char skontrolovať_cloud_soket_adresa_zmeniť_veľkosť[(sizeof(struct cloud_soket_adresa)==16)?1:-1];
typedef char skontrolovať_cloud_soket_adresa_Navigácia[(offsetof(struct cloud_soket_adresa,internetová_adresa)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Create_účastník(int adresa_séria, int 통신방식, int prenos_protokol);
int BIND_adresa(int účastník, const struct soket_adresa *adresa, soket_adresa_dĺžka_Typ dĺžka_VALUE);
intptr_t odoslať_datagram_údaje(int účastník, const void *údaje, size_t položka_COUNT, int výber_VALUE, const struct soket_adresa *adresa, soket_adresa_dĺžka_Typ dĺžka_VALUE);
intptr_t dostať_datagram_údaje(int účastník, void *údaje, size_t položka_COUNT, int výber_VALUE, struct soket_adresa *adresa, soket_adresa_dĺžka_Typ *dĺžka_VALUE);
int 통신주소읽기(int účastník, struct soket_adresa *adresa, soket_adresa_dĺžka_Typ *dĺžka_VALUE);
int spojiť_sieť(int účastník, const struct soket_adresa *adresa, soket_adresa_dĺžka_Typ dĺžka_VALUE);
int 통신연결기다리기(int účastník, int Čakám_COUNT);
int prijať_sieťové_pripojenie(int účastník, struct soket_adresa *adresa, soket_adresa_dĺžka_Typ *dĺžka_VALUE);

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
static inline uint32_t sieť_celé_číslo(uint32_t VALUE) { return ((VALUE & 255u) << 24) | ((VALUE & 0xff00u) << 8) | ((VALUE >> 8) & 0xff00u) | (VALUE >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t VALUE) { return 망차례짧은수(VALUE); }
static inline uint32_t telefón_poradie_celé_číslo(uint32_t VALUE) { return sieť_celé_číslo(VALUE); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return sieť_celé_číslo(x); }
#endif
