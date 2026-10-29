#ifndef JKOROS_SOCKET_H
#define JKOROS_SOCKET_H
#include <sys/types.h>
typedef unsigned int socklen_t;
typedef unsigned short sa_family_t;
struct sockaddr { sa_family_t sa_family; char sa_data[14]; };
#define AF_INET 2
#define SOCK_STREAM 1
#define SOCK_DGRAM 2
#define MSG_DONTWAIT 64
#define SOL_SOCKET 1
#define SO_RCVTIMEO 20
int socket(int 주소체계, int net_soort, int taak_nummer);
int bind(int 파일서술자, const struct sockaddr *ADRES, socklen_t ADRES_tijdsduur);
ssize_t sendto(int 파일서술자, const void *gegevens, size_t byte_AANTAL, int Instellingen,
               const struct sockaddr *ADRES, socklen_t ADRES_tijdsduur);
ssize_t recvfrom(int 파일서술자, void *gegevens, size_t byte_AANTAL, int Instellingen,
                 struct sockaddr *ADRES, socklen_t *ADRES_tijdsduur);
int getsockname(int 파일서술자, struct sockaddr *ADRES, socklen_t *ADRES_tijdsduur);
int setsockopt(int 파일서술자, int laag_WAARDE, int Instellingen_naam, const void *WAARDE, socklen_t WAARDE_tijdsduur);
#endif
