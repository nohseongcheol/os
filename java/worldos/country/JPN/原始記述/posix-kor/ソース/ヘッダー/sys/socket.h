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
int socket(int 番地方式体系, int 通信網種別, int 契約番号);
int bind(int ファイル記述子, const struct sockaddr *番地, socklen_t 番地長さ);
ssize_t sendto(int ファイル記述子, const void *データ, size_t バイト個数, int 設定値,
               const struct sockaddr *番地, socklen_t 番地長さ);
ssize_t recvfrom(int ファイル記述子, void *データ, size_t バイト個数, int 設定値,
                 struct sockaddr *番地, socklen_t *番地長さ);
int getsockname(int ファイル記述子, struct sockaddr *番地, socklen_t *番地長さ);
int setsockopt(int ファイル記述子, int 階層値, int 設定値名前, const void *値, socklen_t 値長さ);
#endif
