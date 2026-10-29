#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 eksekverbar_fil·ekstern_VÆRDI 코드와 연결할 때만 사용한다. */
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

/* Dansk 자료형은 makro_VÆRDI 별칭이 아닌 독립된 구조체다.
 * mail(住所)는 도착할 곳, 갈래는 mail operativsystem_VÆRDI, datagram(電文)은 grænse_VÆRDI 있는 통신 자료다. */
enum netværk_konstant {
    net_serie = 2, strøm_netværk = 1, datagram_socket = 2,
    strøm_transportprotokol = 6, datagram_protokol = 17,
    tilbagekoblingsadresse = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t socket_mail_varighed_Type;
struct socket_mail { uint16_t mail_serie; unsigned char mail_data[14]; };
struct internetadresse_VÆRDI { uint32_t mail_VÆRDI; };
struct net_socket_mail {
    uint16_t mail_serie;
    uint16_t portnummer;
    struct internetadresse_VÆRDI internetadresse;
    unsigned char margen_VÆRDI[8];
};
typedef struct socket_mail socket_mail_Type;
typedef struct net_socket_mail net_socket_mail_Type;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char check_net_socket_mail_tilpasse_størrelse[(sizeof(struct net_socket_mail)==16)?1:-1];
typedef char check_net_socket_mail_Layout[(offsetof(struct net_socket_mail,internetadresse)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int åbne_slutpunkt(int mail_serie, int 통신방식, int overføre_protokol);
int BIND_mail(int slutpunkt, const struct socket_mail *mail, socket_mail_varighed_Type varighed_VÆRDI);
intptr_t maile_datagram_data(int slutpunkt, const void *data, size_t vare_TÆL, int markering_VÆRDI, const struct socket_mail *mail, socket_mail_varighed_Type varighed_VÆRDI);
intptr_t modtage_datagram_data(int slutpunkt, void *data, size_t vare_TÆL, int markering_VÆRDI, struct socket_mail *mail, socket_mail_varighed_Type *varighed_VÆRDI);
int 통신주소읽기(int slutpunkt, struct socket_mail *mail, socket_mail_varighed_Type *varighed_VÆRDI);
int Forbind_netværk(int slutpunkt, const struct socket_mail *mail, socket_mail_varighed_Type varighed_VÆRDI);
int 통신연결기다리기(int slutpunkt, int Venter_TÆL);
int acceptere_netværksforbindelse(int slutpunkt, struct socket_mail *mail, socket_mail_varighed_Type *varighed_VÆRDI);

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
static inline uint16_t 망차례짧은수(uint16_t VÆRDI) { return (uint16_t)((VÆRDI >> 8) | (VÆRDI << 8)); }
static inline uint32_t netværk_heltal(uint32_t VÆRDI) { return ((VÆRDI & 255u) << 24) | ((VÆRDI & 0xff00u) << 8) | ((VÆRDI >> 8) & 0xff00u) | (VÆRDI >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t VÆRDI) { return 망차례짧은수(VÆRDI); }
static inline uint32_t enhed_ordre_heltal(uint32_t VÆRDI) { return netværk_heltal(VÆRDI); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return netværk_heltal(x); }
#endif
