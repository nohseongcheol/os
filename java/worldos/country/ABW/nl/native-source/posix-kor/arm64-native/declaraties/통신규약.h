#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 uitvoerbaar_bestand·extern_WAARDE 코드와 연결할 때만 사용한다. */
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

/* Nederlands 자료형은 macro_WAARDE 별칭이 아닌 독립된 구조체다.
 * ADRES(住所)는 도착할 곳, 갈래는 ADRES besturingssysteem_WAARDE, datagram(電文)은 grens_WAARDE 있는 communicatie 자료다. */
enum net_constante {
    mesh_Gezin = 2, Stream_net = 1, datagramsocket = 2,
    Stream_transportprotocol = 6, datagram_protocol = 17,
    loopback_adres = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t socket_ADRES_tijdsduur_TYPE;
struct socket_ADRES { uint16_t ADRES_Gezin; unsigned char ADRES_gegevens[14]; };
struct internetadres_WAARDE { uint32_t ADRES_WAARDE; };
struct mesh_socket_ADRES {
    uint16_t ADRES_Gezin;
    uint16_t poortnummer;
    struct internetadres_WAARDE internetadres;
    unsigned char marge_WAARDE[8];
};
typedef struct socket_ADRES socket_ADRES_TYPE;
typedef struct mesh_socket_ADRES mesh_socket_ADRES_TYPE;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char cheque_mesh_socket_ADRES_formaat_wijzigen[(sizeof(struct mesh_socket_ADRES)==16)?1:-1];
typedef char cheque_mesh_socket_ADRES_Indeling[(offsetof(struct mesh_socket_ADRES,internetadres)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int maken_eindpunt(int ADRES_Gezin, int communicatie_MODUS, int transfer_protocol);
int BIND_ADRES(int eindpunt, const struct socket_ADRES *ADRES, socket_ADRES_tijdsduur_TYPE tijdsduur_WAARDE);
intptr_t e_mailen_datagram_gegevens(int eindpunt, const void *gegevens, size_t item_AANTAL, int selectie_WAARDE, const struct socket_ADRES *ADRES, socket_ADRES_tijdsduur_TYPE tijdsduur_WAARDE);
intptr_t ontvangen_datagram_gegevens(int eindpunt, void *gegevens, size_t item_AANTAL, int selectie_WAARDE, struct socket_ADRES *ADRES, socket_ADRES_tijdsduur_TYPE *tijdsduur_WAARDE);
int 통신주소읽기(int eindpunt, struct socket_ADRES *ADRES, socket_ADRES_tijdsduur_TYPE *tijdsduur_WAARDE);
int VERBINDEN_net(int eindpunt, const struct socket_ADRES *ADRES, socket_ADRES_tijdsduur_TYPE tijdsduur_WAARDE);
int 통신연결기다리기(int eindpunt, int Wachten_AANTAL);
int accepteren_netwerkverbinding(int eindpunt, struct socket_ADRES *ADRES, socket_ADRES_tijdsduur_TYPE *tijdsduur_WAARDE);

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
static inline uint16_t 망차례짧은수(uint16_t WAARDE) { return (uint16_t)((WAARDE >> 8) | (WAARDE << 8)); }
static inline uint32_t net_geheel_getal(uint32_t WAARDE) { return ((WAARDE & 255u) << 24) | ((WAARDE & 0xff00u) << 8) | ((WAARDE >> 8) & 0xff00u) | (WAARDE >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t WAARDE) { return 망차례짧은수(WAARDE); }
static inline uint32_t mobiel_order_geheel_getal(uint32_t WAARDE) { return net_geheel_getal(WAARDE); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return net_geheel_getal(x); }
#endif
