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
int socket(int 주소체계, int 통신종류, int 규약번호);
int bind(int 파일서술자, const struct sockaddr *salgy, socklen_t salgy_dowamlylyk);
ssize_t sendto(int 파일서술자, const void *maglumat, size_t 바이트수, int Düzümler,
               const struct sockaddr *salgy, socklen_t salgy_dowamlylyk);
ssize_t recvfrom(int 파일서술자, void *maglumat, size_t 바이트수, int Düzümler,
                 struct sockaddr *salgy, socklen_t *salgy_dowamlylyk);
int getsockname(int 파일서술자, struct sockaddr *salgy, socklen_t *salgy_dowamlylyk);
int setsockopt(int 파일서술자, int dereje_baha, int Sazlamalar_at, const void *baha, socklen_t baha_dowamlylyk);
#endif
