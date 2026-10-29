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
int socket(int 주소체계, int rete_Kind, int caso_numero);
int bind(int File_descrittore, const struct sockaddr *e_mail, socklen_t e_mail_durata);
ssize_t sendto(int File_descrittore, const void *dati, size_t byte_CONTA_NUMERI, int Impostazioni,
               const struct sockaddr *e_mail, socklen_t e_mail_durata);
ssize_t recvfrom(int File_descrittore, void *dati, size_t byte_CONTA_NUMERI, int Impostazioni,
                 struct sockaddr *e_mail, socklen_t *e_mail_durata);
int getsockname(int File_descrittore, struct sockaddr *e_mail, socklen_t *e_mail_durata);
int setsockopt(int File_descrittore, int layer_VALORE, int Impostazioni_nome, const void *VALORE, socklen_t VALORE_durata);
#endif
