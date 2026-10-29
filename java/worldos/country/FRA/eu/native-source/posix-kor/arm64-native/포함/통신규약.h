#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 실행파일·외부 코드와 연결할 때만 사용한다. */
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

/* Euskara 자료형은 makro_balio 별칭이 아닌 독립된 구조체다.
 * helbide(住所)는 도착할 곳, 갈래는 helbide sistema_eragile_balio, 전문(電文)은 경계 있는 통신 자료다. */
enum sare_konstante {
    hodei_sorta = 2, Stream_sare = 1, 전문통신 = 2,
    Stream_garraio_protokolo = 6, 전문전송규약 = 17,
    되돌림주소 = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t 통신주소길이형;
struct 통신주소 { uint16_t helbide_sorta; unsigned char helbide_datuak[14]; };
struct Internet_helbide_balio { uint32_t helbide_balio; };
struct 인터넷통신주소 {
    uint16_t helbide_sorta;
    uint16_t ataka_zenbaki;
    struct Internet_helbide_balio Internet_helbide;
    unsigned char marjina_balio[8];
};
typedef struct 통신주소 통신주소형;
typedef struct 인터넷통신주소 인터넷통신주소형;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char 인터넷통신주소크기검사[(sizeof(struct 인터넷통신주소)==16)?1:-1];
typedef char 인터넷통신주소배치검사[(offsetof(struct 인터넷통신주소,Internet_helbide)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int sortu_amaiera_puntu(int helbide_sorta, int 통신방식, int transferitu_protokolo);
int lotu_helbide(int amaiera_puntu, const struct 통신주소 *helbide, 통신주소길이형 luzera_balio);
intptr_t 자료전문보내기(int amaiera_puntu, const void *datuak, size_t elementu_ZENBATU, int hautapen_balio, const struct 통신주소 *helbide, 통신주소길이형 luzera_balio);
intptr_t 자료전문받기(int amaiera_puntu, void *datuak, size_t elementu_ZENBATU, int hautapen_balio, struct 통신주소 *helbide, 통신주소길이형 *luzera_balio);
int 통신주소읽기(int amaiera_puntu, struct 통신주소 *helbide, 통신주소길이형 *luzera_balio);
int KONEKTATU_sare(int amaiera_puntu, const struct 통신주소 *helbide, 통신주소길이형 luzera_balio);
int 통신연결기다리기(int amaiera_puntu, int Zain_ZENBATU);
int onartu_sare_konexio(int amaiera_puntu, struct 통신주소 *helbide, 통신주소길이형 *luzera_balio);

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
static inline uint16_t 망차례짧은수(uint16_t balio) { return (uint16_t)((balio >> 8) | (balio << 8)); }
static inline uint32_t sare_osoko_zenbaki(uint32_t balio) { return ((balio & 255u) << 24) | ((balio & 0xff00u) << 8) | ((balio >> 8) & 0xff00u) | (balio >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t balio) { return 망차례짧은수(balio); }
static inline uint32_t gailu_ordena_osoko_zenbaki(uint32_t balio) { return sare_osoko_zenbaki(balio); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return sare_osoko_zenbaki(x); }
#endif
