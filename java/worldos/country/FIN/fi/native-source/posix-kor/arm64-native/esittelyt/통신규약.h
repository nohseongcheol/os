#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 suoritettava_tiedosto·ulkoinen_ARVO 코드와 연결할 때만 사용한다. */
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

/* suomi 자료형은 makro_ARVO 별칭이 아닌 독립된 구조체다.
 * OSOITE(住所)는 도착할 곳, 갈래는 OSOITE käyttöjärjestelmä_ARVO, datagrammi(電文)은 rajattu_alue_ARVO 있는 통신 자료다. */
enum verkko_vakio {
    pilvi_Perhe = 2, virta_verkko = 1, datagrammivastake = 2,
    virta_kuljetusprotokolla = 6, datagrammi_protokolla = 17,
    silmukkaosoite = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t vastake_OSOITE_kesto_TYYPPI;
struct vastake_OSOITE { uint16_t OSOITE_Perhe; unsigned char OSOITE_data[14]; };
struct Internet_osoite_ARVO { uint32_t OSOITE_ARVO; };
struct pilvi_vastake_OSOITE {
    uint16_t OSOITE_Perhe;
    uint16_t portin_numero;
    struct Internet_osoite_ARVO Internet_osoite;
    unsigned char reunus_ARVO[8];
};
typedef struct vastake_OSOITE vastake_OSOITE_TYYPPI;
typedef struct pilvi_vastake_OSOITE pilvi_vastake_OSOITE_TYYPPI;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char sekki_pilvi_vastake_OSOITE_muuttaa_kokoa[(sizeof(struct pilvi_vastake_OSOITE)==16)?1:-1];
typedef char sekki_pilvi_vastake_OSOITE_Asettelu[(offsetof(struct pilvi_vastake_OSOITE,Internet_osoite)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Luo_päätepiste(int OSOITE_Perhe, int 통신방식, int Siirrä_protokolla);
int BIND_OSOITE(int päätepiste, const struct vastake_OSOITE *OSOITE, vastake_OSOITE_kesto_TYYPPI kesto_ARVO);
intptr_t lähettää_datagrammi_data(int päätepiste, const void *data, size_t kohde_LASKE, int valinta_ARVO, const struct vastake_OSOITE *OSOITE, vastake_OSOITE_kesto_TYYPPI kesto_ARVO);
intptr_t saada_datagrammi_data(int päätepiste, void *data, size_t kohde_LASKE, int valinta_ARVO, struct vastake_OSOITE *OSOITE, vastake_OSOITE_kesto_TYYPPI *kesto_ARVO);
int lukea_vastake_OSOITE(int päätepiste, struct vastake_OSOITE *OSOITE, vastake_OSOITE_kesto_TYYPPI *kesto_ARVO);
int YHDISTÄ_verkko(int päätepiste, const struct vastake_OSOITE *OSOITE, vastake_OSOITE_kesto_TYYPPI kesto_ARVO);
int 통신연결기다리기(int päätepiste, int Odotetaan_LASKE);
int hyväksyä_verkkoyhteys(int päätepiste, struct vastake_OSOITE *OSOITE, vastake_OSOITE_kesto_TYYPPI *kesto_ARVO);

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
static inline uint16_t 망차례짧은수(uint16_t ARVO) { return (uint16_t)((ARVO >> 8) | (ARVO << 8)); }
static inline uint32_t verkko_kokonaisluku(uint32_t ARVO) { return ((ARVO & 255u) << 24) | ((ARVO & 0xff00u) << 8) | ((ARVO >> 8) & 0xff00u) | (ARVO >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t ARVO) { return 망차례짧은수(ARVO); }
static inline uint32_t laite_tilata_kokonaisluku(uint32_t ARVO) { return verkko_kokonaisluku(ARVO); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return verkko_kokonaisluku(x); }
#endif
