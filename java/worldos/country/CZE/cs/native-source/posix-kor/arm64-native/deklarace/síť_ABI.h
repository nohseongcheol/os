#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "Soubor_ABI.h"
/* 표준 ABI는 기존 spustitelný_soubor·externí_HODNOTA 코드와 연결할 때만 사용한다. */
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

/* čeština 자료형은 makro_HODNOTA 별칭이 아닌 독립된 구조체다.
 * Adresa(住所)는 도착할 곳, 갈래는 Adresa operační_systém_HODNOTA, datagram(電文)은 mez_HODNOTA 있는 komunikace 자료다. */
enum síť_konstanta {
    cloud_řada = 2, tok_síť = 1, datagramový_soket = 2,
    tok_transportní_protokol = 6, datagram_protokol = 17,
    adresa_zpětné_smyčky = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t soket_ODKAZ_délka_TYP;
struct soket_ODKAZ { uint16_t ODKAZ_řada; unsigned char ODKAZ_data[14]; };
struct internetová_adresa_HODNOTA { uint32_t ODKAZ_HODNOTA; };
struct cloud_soket_ODKAZ {
    uint16_t ODKAZ_řada;
    uint16_t číslo_portu;
    struct internetová_adresa_HODNOTA internetová_adresa;
    unsigned char okraj_HODNOTA[8];
};
typedef struct soket_ODKAZ soket_ODKAZ_TYP;
typedef struct cloud_soket_ODKAZ cloud_soket_ODKAZ_TYP;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char šek_cloud_soket_ODKAZ_změnit_velikost[(sizeof(struct cloud_soket_ODKAZ)==16)?1:-1];
typedef char šek_cloud_soket_ODKAZ_Navigace[(offsetof(struct cloud_soket_ODKAZ,internetová_adresa)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Create_účastník(int ODKAZ_řada, int komunikace_MODE, int přenos_protokol);
int vázat_ODKAZ(int účastník, const struct soket_ODKAZ *Adresa, soket_ODKAZ_délka_TYP délka_HODNOTA);
intptr_t poslat_datagram_data(int účastník, const void *data, size_t zboží_POČET, int výběr_HODNOTA, const struct soket_ODKAZ *Adresa, soket_ODKAZ_délka_TYP délka_HODNOTA);
intptr_t dostat_datagram_data(int účastník, void *data, size_t zboží_POČET, int výběr_HODNOTA, struct soket_ODKAZ *Adresa, soket_ODKAZ_délka_TYP *délka_HODNOTA);
int 통신주소읽기(int účastník, struct soket_ODKAZ *Adresa, soket_ODKAZ_délka_TYP *délka_HODNOTA);
int spojit_síť(int účastník, const struct soket_ODKAZ *Adresa, soket_ODKAZ_délka_TYP délka_HODNOTA);
int 통신연결기다리기(int účastník, int Čekám_POČET);
int přijmout_síťové_připojení(int účastník, struct soket_ODKAZ *Adresa, soket_ODKAZ_délka_TYP *délka_HODNOTA);

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
static inline uint16_t 망차례짧은수(uint16_t HODNOTA) { return (uint16_t)((HODNOTA >> 8) | (HODNOTA << 8)); }
static inline uint32_t síť_integer(uint32_t HODNOTA) { return ((HODNOTA & 255u) << 24) | ((HODNOTA & 0xff00u) << 8) | ((HODNOTA >> 8) & 0xff00u) | (HODNOTA >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t HODNOTA) { return 망차례짧은수(HODNOTA); }
static inline uint32_t mobilní_pořadí_integer(uint32_t HODNOTA) { return síť_integer(HODNOTA); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return síť_integer(x); }
#endif
