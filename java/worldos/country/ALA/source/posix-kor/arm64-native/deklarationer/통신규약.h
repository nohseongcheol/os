#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 körbar_fil_fil·extern_värde 코드와 연결할 때만 사용한다. */
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

/* Svenska 자료형은 makro_värde 별칭이 아닌 독립된 구조체다.
 * Adress(住所)는 도착할 곳, 갈래는 Adress operativsystem_värde, datagram(電文)은 gräns_värde 있는 kommunikation 자료다. */
enum nätverk_konstant {
    nät_serie = 2, flöde_nätverk = 1, datagramsocket = 2,
    flöde_transportprotokoll = 6, datagram_protokoll = 17,
    loopback_adress = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t socket_ADRESS_längd_Typ;
struct socket_ADRESS { uint16_t ADRESS_serie; unsigned char ADRESS_data[14]; };
struct Internetadress_värde { uint32_t ADRESS_värde; };
struct nät_socket_ADRESS {
    uint16_t ADRESS_serie;
    uint16_t portnummer;
    struct Internetadress_värde Internetadress;
    unsigned char marginal_värde[8];
};
typedef struct socket_ADRESS socket_ADRESS_Typ;
typedef struct nät_socket_ADRESS nät_socket_ADRESS_Typ;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char check_nät_socket_ADRESS_storlek[(sizeof(struct nät_socket_ADRESS)==16)?1:-1];
typedef char check_nät_socket_ADRESS_Layout[(offsetof(struct nät_socket_ADRESS,Internetadress)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Skapa_deltagare(int ADRESS_serie, int kommunikation_läge, int Överför_protokoll);
int BIND_ADRESS(int deltagare, const struct socket_ADRESS *Adress, socket_ADRESS_längd_Typ längd_värde);
intptr_t skicka_datagram_data(int deltagare, const void *data, size_t objekt_ANTAL, int markering_värde, const struct socket_ADRESS *Adress, socket_ADRESS_längd_Typ längd_värde);
intptr_t få_datagram_data(int deltagare, void *data, size_t objekt_ANTAL, int markering_värde, struct socket_ADRESS *Adress, socket_ADRESS_längd_Typ *längd_värde);
int läsa_socket_ADRESS(int deltagare, struct socket_ADRESS *Adress, socket_ADRESS_längd_Typ *längd_värde);
int ANSLUT_nätverk(int deltagare, const struct socket_ADRESS *Adress, socket_ADRESS_längd_Typ längd_värde);
int 통신연결기다리기(int deltagare, int 대기수);
int acceptera_nätverksanslutning(int deltagare, struct socket_ADRESS *Adress, socket_ADRESS_längd_Typ *längd_värde);

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
static inline uint16_t 망차례짧은수(uint16_t värde) { return (uint16_t)((värde >> 8) | (värde << 8)); }
static inline uint32_t nätverk_heltal(uint32_t värde) { return ((värde & 255u) << 24) | ((värde & 0xff00u) << 8) | ((värde >> 8) & 0xff00u) | (värde >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t värde) { return 망차례짧은수(värde); }
static inline uint32_t enhet_order_heltal(uint32_t värde) { return nätverk_heltal(värde); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return nätverk_heltal(x); }
#endif
