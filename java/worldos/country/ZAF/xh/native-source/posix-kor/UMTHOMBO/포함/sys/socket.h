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
int bind(int 파일서술자, const struct sockaddr *idilesi, socklen_t idilesi_ubude);
ssize_t sendto(int 파일서술자, const void *iingcombolo, size_t 바이트수, int Imimiselo,
               const struct sockaddr *idilesi, socklen_t idilesi_ubude);
ssize_t recvfrom(int 파일서술자, void *iingcombolo, size_t 바이트수, int Imimiselo,
                 struct sockaddr *idilesi, socklen_t *idilesi_ubude);
int getsockname(int 파일서술자, struct sockaddr *idilesi, socklen_t *idilesi_ubude);
int setsockopt(int 파일서술자, int ileya_ixabiso, int Iisetingi_igama, const void *ixabiso, socklen_t ixabiso_ubude);
#endif
