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
int bind(int 파일서술자, const struct sockaddr *ଠିକଣା, socklen_t ଠିକଣା_ଦୈର୍ଘ୍ୟ);
ssize_t sendto(int 파일서술자, const void *ଡାଟା, size_t 바이트수, int ବିନ୍ଯାସ,
               const struct sockaddr *ଠିକଣା, socklen_t ଠିକଣା_ଦୈର୍ଘ୍ୟ);
ssize_t recvfrom(int 파일서술자, void *ଡାଟା, size_t 바이트수, int ବିନ୍ଯାସ,
                 struct sockaddr *ଠିକଣା, socklen_t *ଠିକଣା_ଦୈର୍ଘ୍ୟ);
int getsockname(int 파일서술자, struct sockaddr *ଠିକଣା, socklen_t *ଠିକଣା_ଦୈର୍ଘ୍ୟ);
int setsockopt(int 파일서술자, int ସ୍ତର_ମୂଲ୍ୟ, int ସେଟିଂସ୍_ନାମ, const void *ମୂଲ୍ୟ, socklen_t ମୂଲ୍ୟ_ଦୈର୍ଘ୍ୟ);
#endif
