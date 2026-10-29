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
int socket(int 주소체계, int síť_Druh, int případ_číslo);
int bind(int Soubor_popisovač, const struct sockaddr *Adresa, socklen_t ODKAZ_délka);
ssize_t sendto(int Soubor_popisovač, const void *data, size_t bajt_POČET, int Nastavení,
               const struct sockaddr *Adresa, socklen_t ODKAZ_délka);
ssize_t recvfrom(int Soubor_popisovač, void *data, size_t bajt_POČET, int Nastavení,
                 struct sockaddr *Adresa, socklen_t *ODKAZ_délka);
int getsockname(int Soubor_popisovač, struct sockaddr *Adresa, socklen_t *ODKAZ_délka);
int setsockopt(int Soubor_popisovač, int vrstva_HODNOTA, int Nastavení_název, const void *HODNOTA, socklen_t HODNOTA_délka);
#endif
