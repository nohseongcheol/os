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
int socket(int 주소체계, int 통신종류, int sak_nummer);
int bind(int 파일서술자, const struct sockaddr *e_post, socklen_t e_post_lengde);
ssize_t sendto(int 파일서술자, const void *data, size_t byte_ANTALL, int Innstillinger,
               const struct sockaddr *e_post, socklen_t e_post_lengde);
ssize_t recvfrom(int 파일서술자, void *data, size_t byte_ANTALL, int Innstillinger,
                 struct sockaddr *e_post, socklen_t *e_post_lengde);
int getsockname(int 파일서술자, struct sockaddr *e_post, socklen_t *e_post_lengde);
int setsockopt(int 파일서술자, int lag_VERDI, int Innstillinger_navn, const void *VERDI, socklen_t VERDI_lengde);
#endif
