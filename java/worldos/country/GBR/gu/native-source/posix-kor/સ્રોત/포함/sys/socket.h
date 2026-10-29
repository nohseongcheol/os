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
int bind(int 파일서술자, const struct sockaddr *સરનામું, socklen_t સરનામું_લંબાઈ);
ssize_t sendto(int 파일서술자, const void *ડેટા, size_t 바이트수, int સુયોજના,
               const struct sockaddr *સરનામું, socklen_t સરનામું_લંબાઈ);
ssize_t recvfrom(int 파일서술자, void *ડેટા, size_t 바이트수, int સુયોજના,
                 struct sockaddr *સરનામું, socklen_t *સરનામું_લંબાઈ);
int getsockname(int 파일서술자, struct sockaddr *સરનામું, socklen_t *સરનામું_લંબાઈ);
int setsockopt(int 파일서술자, int થર_મૂલ્ય, int સેટિંગ્સ_નામ, const void *મૂલ્ય, socklen_t મૂલ્ય_લંબાઈ);
#endif
