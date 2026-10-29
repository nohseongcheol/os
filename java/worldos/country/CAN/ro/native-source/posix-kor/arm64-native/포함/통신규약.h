#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·extern_VALUE 코드와 연결할 때만 사용한다. */
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

/* Română 자료형은 macrocomandă_VALUE 별칭이 아닌 독립된 구조체다.
 * adresa(住所)는 도착할 곳, 갈래는 adresa sistem_de_operare_VALUE, diagramă_informații(電文)은 경계 있는 통신 자료다. */
enum rețea_constantă {
    cloud_Familie = 2, flux_rețea = 1, racord_diagramă_informații = 2,
    flux_protocol_de_transport = 6, diagramă_informații_protocol = 17,
    adresă_de_întoarcere_în_buclă = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t adresa_Familie; unsigned char adresa_date[14]; };
struct adresă_internet_VALUE { uint32_t adresa_VALUE; };
struct 인터넷통신주소 {
    uint16_t adresa_Familie;
    uint16_t număr_port;
    struct adresă_internet_VALUE adresă_internet;
    unsigned char margine_VALUE[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,adresă_internet)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int crea_participant(int adresa_Familie, int 통신방식, int Transfer_protocol);
int BIND_adresa(int participant, const struct 통신주소 *adresa, 통신주소길이형 lungime_VALUE);
intptr_t trimite_diagramă_informații_date(int participant, const void *date, size_t element_COUNT, int selecție_VALUE, const struct 통신주소 *adresa, 통신주소길이형 lungime_VALUE);
intptr_t primi_diagramă_informații_date(int participant, void *date, size_t element_COUNT, int selecție_VALUE, struct 통신주소 *adresa, 통신주소길이형 *lungime_VALUE);
int 통신주소읽기(int participant, struct 통신주소 *adresa, 통신주소길이형 *lungime_VALUE);
int conecta_rețea(int participant, const struct 통신주소 *adresa, 통신주소길이형 lungime_VALUE);
int 통신연결기다리기(int participant, int Aștept_COUNT);
int accepta_conexiune_rețea(int participant, struct 통신주소 *adresa, 통신주소길이형 *lungime_VALUE);

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
static inline uint32_t rețea_întreg(uint32_t VALUE) { return ((VALUE & 255u) << 24) | ((VALUE & 0xff00u) << 8) | ((VALUE >> 8) & 0xff00u) | (VALUE >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t VALUE) { return 망차례짧은수(VALUE); }
static inline uint32_t mobil_ordine_întreg(uint32_t VALUE) { return rețea_întreg(VALUE); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return rețea_întreg(x); }
#endif
