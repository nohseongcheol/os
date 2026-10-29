#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 végrehajtható_Fájl·külső_ÉRTÉK 코드와 연결할 때만 사용한다. */
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

/* magyar 자료형은 makró_ÉRTÉK 별칭이 아닌 독립된 구조체다.
 * CÍM(住所)는 도착할 곳, 갈래는 CÍM operációs_rendszer_ÉRTÉK, datagram(電文)은 határ_ÉRTÉK 있는 kommunikáció 자료다. */
enum hálózat_állandó {
    háló_Család = 2, Stream_hálózat = 1, datagram_szoftvercsatorna = 2,
    Stream_átviteli_protokoll = 6, datagram_protokoll = 17,
    visszacsatolási_cím = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t szoftvercsatorna_CÍM_hossz_beír;
struct szoftvercsatorna_CÍM { uint16_t CÍM_Család; unsigned char CÍM_adat[14]; };
struct internetcím_ÉRTÉK { uint32_t CÍM_ÉRTÉK; };
struct háló_szoftvercsatorna_CÍM {
    uint16_t CÍM_Család;
    uint16_t portszám;
    struct internetcím_ÉRTÉK internetcím;
    unsigned char margó_ÉRTÉK[8];
};
typedef struct szoftvercsatorna_CÍM szoftvercsatorna_CÍM_beír;
typedef struct háló_szoftvercsatorna_CÍM háló_szoftvercsatorna_CÍM_beír;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char csekk_háló_szoftvercsatorna_CÍM_méretez[(sizeof(struct háló_szoftvercsatorna_CÍM)==16)?1:-1];
typedef char csekk_háló_szoftvercsatorna_CÍM_Navigáció[(offsetof(struct háló_szoftvercsatorna_CÍM,internetcím)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int készít_végpont(int CÍM_Család, int kommunikáció_mód, int átvisz_protokoll);
int BIND_CÍM(int végpont, const struct szoftvercsatorna_CÍM *CÍM, szoftvercsatorna_CÍM_hossz_beír hossz_ÉRTÉK);
intptr_t küld_datagram_adat(int végpont, const void *adat, size_t cikk_DARAB, int kijelölés_ÉRTÉK, const struct szoftvercsatorna_CÍM *CÍM, szoftvercsatorna_CÍM_hossz_beír hossz_ÉRTÉK);
intptr_t fogad_datagram_adat(int végpont, void *adat, size_t cikk_DARAB, int kijelölés_ÉRTÉK, struct szoftvercsatorna_CÍM *CÍM, szoftvercsatorna_CÍM_hossz_beír *hossz_ÉRTÉK);
int 통신주소읽기(int végpont, struct szoftvercsatorna_CÍM *CÍM, szoftvercsatorna_CÍM_hossz_beír *hossz_ÉRTÉK);
int KAPCSOLAT_hálózat(int végpont, const struct szoftvercsatorna_CÍM *CÍM, szoftvercsatorna_CÍM_hossz_beír hossz_ÉRTÉK);
int 통신연결기다리기(int végpont, int Várok_DARAB);
int elfogad_hálózati_kapcsolat(int végpont, struct szoftvercsatorna_CÍM *CÍM, szoftvercsatorna_CÍM_hossz_beír *hossz_ÉRTÉK);

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
static inline uint16_t 망차례짧은수(uint16_t ÉRTÉK) { return (uint16_t)((ÉRTÉK >> 8) | (ÉRTÉK << 8)); }
static inline uint32_t hálózat_egész_szám(uint32_t ÉRTÉK) { return ((ÉRTÉK & 255u) << 24) | ((ÉRTÉK & 0xff00u) << 8) | ((ÉRTÉK >> 8) & 0xff00u) | (ÉRTÉK >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t ÉRTÉK) { return 망차례짧은수(ÉRTÉK); }
static inline uint32_t mobil_rendel_egész_szám(uint32_t ÉRTÉK) { return hálózat_egész_szám(ÉRTÉK); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return hálózat_egész_szám(x); }
#endif
