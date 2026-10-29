#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "Dosya_ABI.h"
/* 표준 ABI는 기존 çalıştırılabilir·dış_değer 코드와 연결할 때만 사용한다. */
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

/* Türkçe 자료형은 makro_değer 별칭이 아닌 독립된 구조체다.
 * ADRES(住所)는 도착할 곳, 갈래는 ADRES işletim_sistemi_değer, veri_birimi(電文)은 sınır_değer 있는 iletişim 자료다. */
enum ağ_sabit {
    bulut_Aile = 2, akış_ağ = 1, veri_birimi_yuvası = 2,
    akış_aktarım_protokolü = 6, veri_birimi_protokol = 17,
    geri_döngü_adresi = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t yuva_ADRES_süre_TÜR;
struct yuva_ADRES { uint16_t ADRES_Aile; unsigned char ADRES_veri[14]; };
struct İnternet_adresi_değer { uint32_t ADRES_değer; };
struct bulut_yuva_ADRES {
    uint16_t ADRES_Aile;
    uint16_t bağlantı_noktası_numarası;
    struct İnternet_adresi_değer İnternet_adresi;
    unsigned char dış_boşluk_değer[8];
};
typedef struct yuva_ADRES yuva_ADRES_TÜR;
typedef struct bulut_yuva_ADRES bulut_yuva_ADRES_TÜR;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char çek_bulut_yuva_ADRES_boyutlandırmak[(sizeof(struct bulut_yuva_ADRES)==16)?1:-1];
typedef char çek_bulut_yuva_ADRES_Düzen[(offsetof(struct bulut_yuva_ADRES,İnternet_adresi)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int açmak_uç_nokta(int ADRES_Aile, int iletişim_mod, int devir_protokol);
int BIND_ADRES(int uç_nokta, const struct yuva_ADRES *ADRES, yuva_ADRES_süre_TÜR süre_değer);
intptr_t göndermek_veri_birimi_veri(int uç_nokta, const void *veri, size_t öğe_BAĞ_DEĞ_SAY, int seçim_değer, const struct yuva_ADRES *ADRES, yuva_ADRES_süre_TÜR süre_değer);
intptr_t almak_veri_birimi_veri(int uç_nokta, void *veri, size_t öğe_BAĞ_DEĞ_SAY, int seçim_değer, struct yuva_ADRES *ADRES, yuva_ADRES_süre_TÜR *süre_değer);
int 통신주소읽기(int uç_nokta, struct yuva_ADRES *ADRES, yuva_ADRES_süre_TÜR *süre_değer);
int bağla_ağ(int uç_nokta, const struct yuva_ADRES *ADRES, yuva_ADRES_süre_TÜR süre_değer);
int 통신연결기다리기(int uç_nokta, int Bekliyor_BAĞ_DEĞ_SAY);
int kabul_etmek_ağ_bağlantısı(int uç_nokta, struct yuva_ADRES *ADRES, yuva_ADRES_süre_TÜR *süre_değer);

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
static inline uint16_t 망차례짧은수(uint16_t değer) { return (uint16_t)((değer >> 8) | (değer << 8)); }
static inline uint32_t ağ_bilgi(uint32_t değer) { return ((değer & 255u) << 24) | ((değer & 0xff00u) << 8) | ((değer >> 8) & 0xff00u) | (değer >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t değer) { return 망차례짧은수(değer); }
static inline uint32_t cihaz_düzen_bilgi(uint32_t değer) { return ağ_bilgi(değer); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return ağ_bilgi(x); }
#endif
