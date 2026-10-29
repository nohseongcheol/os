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
int socket(int lượcĐồĐịaChỉ, int loạiMạng, int sốQuyƯớc);
int bind(int bộMôTảTệp, const struct sockaddr *địaChỉ, socklen_t độDàiĐịaChỉ);
ssize_t sendto(int bộMôTảTệp, const void *DữLiệu, size_t sốLượngByte, int cácThiếtLập,
               const struct sockaddr *địaChỉ, socklen_t độDàiĐịaChỉ);
ssize_t recvfrom(int bộMôTảTệp, void *DữLiệu, size_t sốLượngByte, int cácThiếtLập,
                 struct sockaddr *địaChỉ, socklen_t *độDàiĐịaChỉ);
int getsockname(int bộMôTảTệp, struct sockaddr *địaChỉ, socklen_t *độDàiĐịaChỉ);
int setsockopt(int bộMôTảTệp, int giáTrịTầng, int tênCácThiếtLập, const void *giáTrị, socklen_t độDàiGiáTrị);
#endif
