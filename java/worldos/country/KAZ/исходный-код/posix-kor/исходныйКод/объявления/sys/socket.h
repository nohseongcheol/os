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
int socket(int 주소체계, int сеть_Вид, int 규약번호);
int bind(int файл_дескриптор, const struct sockaddr *АДРЕС, socklen_t АДРЕС_длина);
ssize_t sendto(int файл_дескриптор, const void *данные, size_t байт_СЧЁТ, int Настройки,
               const struct sockaddr *АДРЕС, socklen_t АДРЕС_длина);
ssize_t recvfrom(int файл_дескриптор, void *данные, size_t байт_СЧЁТ, int Настройки,
                 struct sockaddr *АДРЕС, socklen_t *АДРЕС_длина);
int getsockname(int файл_дескриптор, struct sockaddr *АДРЕС, socklen_t *АДРЕС_длина);
int setsockopt(int файл_дескриптор, int слой_ЗНАЧЕН, int Настройки_имя, const void *ЗНАЧЕН, socklen_t ЗНАЧЕН_длина);
#endif
