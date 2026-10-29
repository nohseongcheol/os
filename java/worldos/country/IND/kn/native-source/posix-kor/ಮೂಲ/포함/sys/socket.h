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
int bind(int 파일서술자, const struct sockaddr *ಇಮೇಲ್, socklen_t ಇಮೇಲ್_ಉದ್ದ);
ssize_t sendto(int 파일서술자, const void *ಡೇಟಾ, size_t 바이트수, int ಸಿದ್ಧತೆಗಳು,
               const struct sockaddr *ಇಮೇಲ್, socklen_t ಇಮೇಲ್_ಉದ್ದ);
ssize_t recvfrom(int 파일서술자, void *ಡೇಟಾ, size_t 바이트수, int ಸಿದ್ಧತೆಗಳು,
                 struct sockaddr *ಇಮೇಲ್, socklen_t *ಇಮೇಲ್_ಉದ್ದ);
int getsockname(int 파일서술자, struct sockaddr *ಇಮೇಲ್, socklen_t *ಇಮೇಲ್_ಉದ್ದ);
int setsockopt(int 파일서술자, int ಪದರ_ಮೌಲ್ಯ, int ಸೆಟ್ಟಿಂಗ್ಸ್_ಹೆಸರು, const void *ಮೌಲ್ಯ, socklen_t ಮೌಲ್ಯ_ಉದ್ದ);
#endif
