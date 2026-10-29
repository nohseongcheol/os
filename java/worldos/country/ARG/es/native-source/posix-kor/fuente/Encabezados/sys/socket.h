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
int socket(int esquemaDirección, int claseTipoRed, int númeroContrato);
int bind(int descriptorArchivo, const struct sockaddr *dirección, socklen_t longitudDirección);
ssize_t sendto(int descriptorArchivo, const void *Datos, size_t númeroElementosByte, int ajustes,
               const struct sockaddr *dirección, socklen_t longitudDirección);
ssize_t recvfrom(int descriptorArchivo, void *Datos, size_t númeroElementosByte, int ajustes,
                 struct sockaddr *dirección, socklen_t *longitudDirección);
int getsockname(int descriptorArchivo, struct sockaddr *dirección, socklen_t *longitudDirección);
int setsockopt(int descriptorArchivo, int valorCapa, int nombreAjustes, const void *valor, socklen_t longitudValor);
#endif
