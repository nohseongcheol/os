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
int socket(int adresseSchema, int netzwerkArt, int vertragNummer);
int bind(int dateiDeskriptor, const struct sockaddr *adresse, socklen_t adresseLänge);
ssize_t sendto(int dateiDeskriptor, const void *Daten, size_t byteAnzahl, int einstellungen,
               const struct sockaddr *adresse, socklen_t adresseLänge);
ssize_t recvfrom(int dateiDeskriptor, void *Daten, size_t byteAnzahl, int einstellungen,
                 struct sockaddr *adresse, socklen_t *adresseLänge);
int getsockname(int dateiDeskriptor, struct sockaddr *adresse, socklen_t *adresseLänge);
int setsockopt(int dateiDeskriptor, int schichtWert, int einstellungenName, const void *Wert, socklen_t wertLänge);
#endif
