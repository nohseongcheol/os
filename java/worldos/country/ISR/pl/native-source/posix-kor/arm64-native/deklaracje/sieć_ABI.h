#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "Plik_ABI.h"
/* 표준 ABI는 기존 plik_wykonywalny·zewnętrzny_WARTOŚĆ 코드와 연결할 때만 사용한다. */
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

/* polski 자료형은 makro_WARTOŚĆ 별칭이 아닌 독립된 구조체다.
 * Adres(住所)는 도착할 곳, 갈래는 Adres system_operacyjny_WARTOŚĆ, datagram(電文)은 granica_WARTOŚĆ 있는 komunikacja 자료다. */
enum sieć_stała {
    chmura_Rodzina = 2, Stream_sieć = 1, gniazdo_do_przesyłania_datagramów = 2,
    Stream_protokół_transportu = 6, datagram_protokół = 17,
    adres_sprzężenia_zwrotnego = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t gniazdo_ADRES_długość_TYP;
struct gniazdo_ADRES { uint16_t ADRES_Rodzina; unsigned char ADRES_dane[14]; };
struct adres_internetowy_WARTOŚĆ { uint32_t ADRES_WARTOŚĆ; };
struct chmura_gniazdo_ADRES {
    uint16_t ADRES_Rodzina;
    uint16_t numer_portu;
    struct adres_internetowy_WARTOŚĆ adres_internetowy;
    unsigned char margines_WARTOŚĆ[8];
};
typedef struct gniazdo_ADRES gniazdo_ADRES_TYP;
typedef struct chmura_gniazdo_ADRES chmura_gniazdo_ADRES_TYP;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char czek_chmura_gniazdo_ADRES_zmienić_rozmiar[(sizeof(struct chmura_gniazdo_ADRES)==16)?1:-1];
typedef char czek_chmura_gniazdo_ADRES_Układ[(offsetof(struct chmura_gniazdo_ADRES,adres_internetowy)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Twórca_uczestnik(int ADRES_Rodzina, int komunikacja_tryb, int transfer_protokół);
int BIND_ADRES(int uczestnik, const struct gniazdo_ADRES *Adres, gniazdo_ADRES_długość_TYP długość_WARTOŚĆ);
intptr_t wysłać_datagram_dane(int uczestnik, const void *dane, size_t towar_ILE_LICZB, int zaznaczenie_WARTOŚĆ, const struct gniazdo_ADRES *Adres, gniazdo_ADRES_długość_TYP długość_WARTOŚĆ);
intptr_t odbierać_datagram_dane(int uczestnik, void *dane, size_t towar_ILE_LICZB, int zaznaczenie_WARTOŚĆ, struct gniazdo_ADRES *Adres, gniazdo_ADRES_długość_TYP *długość_WARTOŚĆ);
int 통신주소읽기(int uczestnik, struct gniazdo_ADRES *Adres, gniazdo_ADRES_długość_TYP *długość_WARTOŚĆ);
int POŁĄCZ_sieć(int uczestnik, const struct gniazdo_ADRES *Adres, gniazdo_ADRES_długość_TYP długość_WARTOŚĆ);
int 통신연결기다리기(int uczestnik, int Czekam_ILE_LICZB);
int akceptować_połączenie_sieciowe(int uczestnik, struct gniazdo_ADRES *Adres, gniazdo_ADRES_długość_TYP *długość_WARTOŚĆ);

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
static inline uint16_t 망차례짧은수(uint16_t WARTOŚĆ) { return (uint16_t)((WARTOŚĆ >> 8) | (WARTOŚĆ << 8)); }
static inline uint32_t sieć_liczba_całkowita(uint32_t WARTOŚĆ) { return ((WARTOŚĆ & 255u) << 24) | ((WARTOŚĆ & 0xff00u) << 8) | ((WARTOŚĆ >> 8) & 0xff00u) | (WARTOŚĆ >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t WARTOŚĆ) { return 망차례짧은수(WARTOŚĆ); }
static inline uint32_t urządzenie_zamówić_liczba_całkowita(uint32_t WARTOŚĆ) { return sieć_liczba_całkowita(WARTOŚĆ); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return sieć_liczba_całkowita(x); }
#endif
