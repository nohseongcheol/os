#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 kjørbar_fil·ekstern_VERDI 코드와 연결할 때만 사용한다. */
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

/* norsk 자료형은 makro_VERDI 별칭이 아닌 독립된 구조체다.
 * e_post(住所)는 도착할 곳, 갈래는 e_post operativsystem_VERDI, datagram(電文)은 grense_VERDI 있는 통신 자료다. */
enum nettverk_konstant {
    sky_serie = 2, strøm_nettverk = 1, datagramsocket = 2,
    strøm_transportprotokoll = 6, datagram_protokoll = 17,
    tilbakekoblingsadresse = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t socket_e_post_lengde_Type;
struct socket_e_post { uint16_t e_post_serie; unsigned char e_post_data[14]; };
struct Internett_adresse_VERDI { uint32_t e_post_VERDI; };
struct sky_socket_e_post {
    uint16_t e_post_serie;
    uint16_t portnummer;
    struct Internett_adresse_VERDI Internett_adresse;
    unsigned char marg_VERDI[8];
};
typedef struct socket_e_post socket_e_post_Type;
typedef struct sky_socket_e_post sky_socket_e_post_Type;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char sjekk_sky_socket_e_post_skalere[(sizeof(struct sky_socket_e_post)==16)?1:-1];
typedef char sjekk_sky_socket_e_post_Oppsett[(offsetof(struct sky_socket_e_post,Internett_adresse)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int åpne_deltaker(int e_post_serie, int 통신방식, int overføre_protokoll);
int BIND_e_post(int deltaker, const struct socket_e_post *e_post, socket_e_post_lengde_Type lengde_VERDI);
intptr_t sende_datagram_data(int deltaker, const void *data, size_t vare_ANTALL, int merket_område_VERDI, const struct socket_e_post *e_post, socket_e_post_lengde_Type lengde_VERDI);
intptr_t motta_datagram_data(int deltaker, void *data, size_t vare_ANTALL, int merket_område_VERDI, struct socket_e_post *e_post, socket_e_post_lengde_Type *lengde_VERDI);
int 통신주소읽기(int deltaker, struct socket_e_post *e_post, socket_e_post_lengde_Type *lengde_VERDI);
int KOBLE_TIL_nettverk(int deltaker, const struct socket_e_post *e_post, socket_e_post_lengde_Type lengde_VERDI);
int 통신연결기다리기(int deltaker, int Venter_ANTALL);
int godta_nettverkstilkobling(int deltaker, struct socket_e_post *e_post, socket_e_post_lengde_Type *lengde_VERDI);

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
static inline uint16_t 망차례짧은수(uint16_t VERDI) { return (uint16_t)((VERDI >> 8) | (VERDI << 8)); }
static inline uint32_t nettverk_heltall(uint32_t VERDI) { return ((VERDI & 255u) << 24) | ((VERDI & 0xff00u) << 8) | ((VERDI >> 8) & 0xff00u) | (VERDI >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t VERDI) { return 망차례짧은수(VERDI); }
static inline uint32_t enhet_ordre_heltall(uint32_t VERDI) { return nettverk_heltall(VERDI); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return nettverk_heltall(x); }
#endif
