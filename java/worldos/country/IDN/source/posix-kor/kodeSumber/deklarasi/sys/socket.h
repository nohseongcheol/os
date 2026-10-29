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
int bind(int 파일서술자, const struct sockaddr *surel, socklen_t surel_panjang);
ssize_t sendto(int 파일서술자, const void *data, size_t byte_COUNT, int Konfigurasi,
               const struct sockaddr *surel, socklen_t surel_panjang);
ssize_t recvfrom(int 파일서술자, void *data, size_t byte_COUNT, int Konfigurasi,
                 struct sockaddr *surel, socklen_t *surel_panjang);
int getsockname(int 파일서술자, struct sockaddr *surel, socklen_t *surel_panjang);
int setsockopt(int 파일서술자, int lapisan_VALUE, int Pengaturan_nama, const void *VALUE, socklen_t VALUE_panjang);
#endif
