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
int socket(int schémaAdresse, int genreRéseau, int numéroContrat);
int bind(int descripteurFichier, const struct sockaddr *adresse, socklen_t longueurAdresse);
ssize_t sendto(int descripteurFichier, const void *Données, size_t nombreÉlémentsOctet, int réglages,
               const struct sockaddr *adresse, socklen_t longueurAdresse);
ssize_t recvfrom(int descripteurFichier, void *Données, size_t nombreÉlémentsOctet, int réglages,
                 struct sockaddr *adresse, socklen_t *longueurAdresse);
int getsockname(int descripteurFichier, struct sockaddr *adresse, socklen_t *longueurAdresse);
int setsockopt(int descripteurFichier, int valeurCouche, int nomRéglages, const void *valeur, socklen_t longueurValeur);
#endif
