#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "DateiABI.h"
/* 표준 ABI는 기존 ausführdateiDatei·externWert 코드와 연결할 때만 사용한다. */
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

/* Deutsch 자료형은 makroWert 별칭이 아닌 독립된 구조체다.
 * adresse(住所)는 도착할 곳, 갈래는 adresse betriebSystemWert, datagramm(電文)은 grenzstelleWert 있는 Kommunikation 자료다. */
enum netzwerkKonstante {
    InternetFamilie = 2, DatenstromNetzwerk = 1, DatagrammNetzbuchse = 2,
    datenstromBeförderungProtokoll = 6, DatagrammProtokoll = 17,
    rückschleifeAdresse = 0x7f000001u, alleVerbindungAdressen = 0, VersuchenErneutFehler = 11
};
typedef uint32_t netzbuchseAdresseLängeTyp;
struct NetzbuchseAdresse { uint16_t adresseFamilie; unsigned char adresseDaten[14]; };
struct internetAdresseWert { uint32_t adresseWert; };
struct InternetNetzbuchseAdresse {
    uint16_t adresseFamilie;
    uint16_t portNummer;
    struct internetAdresseWert InternetAdresse;
    unsigned char randWert[8];
};
typedef struct NetzbuchseAdresse netzbuchseAdresseTyp;
typedef struct InternetNetzbuchseAdresse internetNetzbuchseAdresseTyp;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char internetNetzbuchseAdresseGrößePrüfen[(sizeof(struct InternetNetzbuchseAdresse)==16)?1:-1];
typedef char internetNetzbuchseAdresseAnordnungPrüfen[(offsetof(struct InternetNetzbuchseAdresse,InternetAdresse)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int endpunktErstellen(int adresseFamilie, int kommunikationBetriebsart, int übertragungProtokoll);
int adresseZuordnen(int endpunkt, const struct NetzbuchseAdresse *adresse, netzbuchseAdresseLängeTyp Länge);
intptr_t datagrammDatenSenden(int endpunkt, const void *Daten, size_t elementeintragAnzahl, int auswahlWert, const struct NetzbuchseAdresse *adresse, netzbuchseAdresseLängeTyp Länge);
intptr_t datagrammDatenEmpfangen(int endpunkt, void *Daten, size_t elementeintragAnzahl, int auswahlWert, struct NetzbuchseAdresse *adresse, netzbuchseAdresseLängeTyp *Länge);
int netzbuchseAdresseLesen(int endpunkt, struct NetzbuchseAdresse *adresse, netzbuchseAdresseLängeTyp *Länge);
int netzwerkVerbinden(int endpunkt, const struct NetzbuchseAdresse *adresse, netzbuchseAdresseLängeTyp Länge);
int fürNetzwerkVerbindungWarten(int endpunkt, int wartendAnzahl);
int netzwerkVerbindungAnnehmen(int endpunkt, struct NetzbuchseAdresse *adresse, netzbuchseAdresseLängeTyp *Länge);

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
static inline uint16_t netzwerkKurz(uint16_t Wert) { return (uint16_t)((Wert >> 8) | (Wert << 8)); }
static inline uint32_t netzwerkGanzzahl(uint32_t Wert) { return ((Wert & 255u) << 24) | ((Wert & 0xff00u) << 8) | ((Wert >> 8) & 0xff00u) | (Wert >> 24); }
static inline uint16_t gerätReihenfolgeKurz(uint16_t Wert) { return netzwerkKurz(Wert); }
static inline uint32_t gerätReihenfolgeGanzzahl(uint32_t Wert) { return netzwerkGanzzahl(Wert); }
static inline uint16_t pk_htons(uint16_t x) { return netzwerkKurz(x); }
static inline uint32_t pk_htonl(uint32_t x) { return netzwerkGanzzahl(x); }
#endif
