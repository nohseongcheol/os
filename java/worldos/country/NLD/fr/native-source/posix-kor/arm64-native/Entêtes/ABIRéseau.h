#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "ABIFichier.h"
/* 표준 ABI는 기존 fichierCodeExécutable·valeurExtérieur 코드와 연결할 때만 사용한다. */
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

/* français 자료형은 valeurMacro 별칭이 아닌 독립된 구조체다.
 * adresse(住所)는 도착할 곳, 갈래는 adresse valeurSystèmeExploitation, datagramme(電文)은 valeurFrontière 있는 Communication 자료다. */
enum constanteRéseau {
    FamilleInternet = 2, RéseauFlux = 1, PriseRéseauDatagramme = 2,
    protocoleTransportFlux = 6, ProtocoleDatagramme = 17,
    adresseBoucleRetour = 0x7f000001u, adressesConnexionTous = 0, ErreurEncoreEssayer = 11
};
typedef uint32_t typeLongueurAdressePriseRéseau;
struct AdressePriseRéseau { uint16_t familleAdresse; unsigned char donnéesAdresse[14]; };
struct valeurAdresseInternet { uint32_t valeurAdresse; };
struct AdressePriseRéseauInternet {
    uint16_t familleAdresse;
    uint16_t numéroPort;
    struct valeurAdresseInternet AdresseInternet;
    unsigned char valeurMarge[8];
};
typedef struct AdressePriseRéseau typeAdressePriseRéseau;
typedef struct AdressePriseRéseauInternet typeAdressePriseRéseauInternet;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char contrôlerTailleAdressePriseRéseauInternet[(sizeof(struct AdressePriseRéseauInternet)==16)?1:-1];
typedef char contrôlerDispositionAdressePriseRéseauInternet[(offsetof(struct AdressePriseRéseauInternet,AdresseInternet)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int créerExtrémité(int familleAdresse, int modeCommunication, int protocoleTransfert);
int associerAdresse(int extrémité, const struct AdressePriseRéseau *adresse, typeLongueurAdressePriseRéseau longueur);
intptr_t envoyerDonnéesDatagramme(int extrémité, const void *Données, size_t nombreÉlémentsÉlémentListe, int valeurSélection, const struct AdressePriseRéseau *adresse, typeLongueurAdressePriseRéseau longueur);
intptr_t recevoirDonnéesDatagramme(int extrémité, void *Données, size_t nombreÉlémentsÉlémentListe, int valeurSélection, struct AdressePriseRéseau *adresse, typeLongueurAdressePriseRéseau *longueur);
int lireAdressePriseRéseau(int extrémité, struct AdressePriseRéseau *adresse, typeLongueurAdressePriseRéseau *longueur);
int connecterRéseau(int extrémité, const struct AdressePriseRéseau *adresse, typeLongueurAdressePriseRéseau longueur);
int attendreConnexionRéseauPour(int extrémité, int nombreÉlémentsAttenteEnCours);
int accepterConnexionRéseau(int extrémité, struct AdressePriseRéseau *adresse, typeLongueurAdressePriseRéseau *longueur);

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
static inline uint16_t courtRéseau(uint16_t valeur) { return (uint16_t)((valeur >> 8) | (valeur << 8)); }
static inline uint32_t entierRéseau(uint32_t valeur) { return ((valeur & 255u) << 24) | ((valeur & 0xff00u) << 8) | ((valeur >> 8) & 0xff00u) | (valeur >> 24); }
static inline uint16_t courtOrdrePériphérique(uint16_t valeur) { return courtRéseau(valeur); }
static inline uint32_t entierOrdrePériphérique(uint32_t valeur) { return entierRéseau(valeur); }
static inline uint16_t pk_htons(uint16_t x) { return courtRéseau(x); }
static inline uint32_t pk_htonl(uint32_t x) { return entierRéseau(x); }
#endif
