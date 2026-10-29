#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "File_ABI.h"
/* 표준 ABI는 기존 eseguibile·esterno_VALORE 코드와 연결할 때만 사용한다. */
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

/* Italiano 자료형은 macro_VALORE 별칭이 아닌 독립된 구조체다.
 * e_mail(住所)는 도착할 곳, 갈래는 e_mail sistema_operativo_VALORE, datagramma(電文)은 limite_VALORE 있는 comunicazione 자료다. */
enum rete_costante {
    cloud_serie = 2, Stream_rete = 1, socket_di_datagramma = 2,
    Stream_protocollo_di_trasporto = 6, datagramma_protocollo = 17,
    indirizzo_di_loopback = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t socket_e_mail_durata_TIPO;
struct socket_e_mail { uint16_t e_mail_serie; unsigned char e_mail_dati[14]; };
struct indirizzo_Internet_VALORE { uint32_t e_mail_VALORE; };
struct cloud_socket_e_mail {
    uint16_t e_mail_serie;
    uint16_t numero_di_porta;
    struct indirizzo_Internet_VALORE indirizzo_Internet;
    unsigned char margine_VALORE[8];
};
typedef struct socket_e_mail socket_e_mail_TIPO;
typedef struct cloud_socket_e_mail cloud_socket_e_mail_TIPO;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char assegno_cloud_socket_e_mail_ridimensionare[(sizeof(struct cloud_socket_e_mail)==16)?1:-1];
typedef char assegno_cloud_socket_e_mail_Layout[(offsetof(struct cloud_socket_e_mail,indirizzo_Internet)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Crea_endpoint(int e_mail_serie, int comunicazione_MODA, int trasferire_protocollo);
int BIND_e_mail(int endpoint, const struct socket_e_mail *e_mail, socket_e_mail_durata_TIPO durata_VALORE);
intptr_t inviare_datagramma_dati(int endpoint, const void *dati, size_t articolo_CONTA_NUMERI, int selezione_VALORE, const struct socket_e_mail *e_mail, socket_e_mail_durata_TIPO durata_VALORE);
intptr_t ricevere_datagramma_dati(int endpoint, void *dati, size_t articolo_CONTA_NUMERI, int selezione_VALORE, struct socket_e_mail *e_mail, socket_e_mail_durata_TIPO *durata_VALORE);
int 통신주소읽기(int endpoint, struct socket_e_mail *e_mail, socket_e_mail_durata_TIPO *durata_VALORE);
int CONNETTI_rete(int endpoint, const struct socket_e_mail *e_mail, socket_e_mail_durata_TIPO durata_VALORE);
int 통신연결기다리기(int endpoint, int In_attesa_CONTA_NUMERI);
int accettare_connessione_di_rete(int endpoint, struct socket_e_mail *e_mail, socket_e_mail_durata_TIPO *durata_VALORE);

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
static inline uint16_t 망차례짧은수(uint16_t VALORE) { return (uint16_t)((VALORE >> 8) | (VALORE << 8)); }
static inline uint32_t rete_intero(uint32_t VALORE) { return ((VALORE & 255u) << 24) | ((VALORE & 0xff00u) << 8) | ((VALORE >> 8) & 0xff00u) | (VALORE >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t VALORE) { return 망차례짧은수(VALORE); }
static inline uint32_t cellulare_ordine_intero(uint32_t VALORE) { return rete_intero(VALORE); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return rete_intero(x); }
#endif
