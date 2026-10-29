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
int socket(int 地址方案, int 网络种类, int 契约编号);
int bind(int 文件描述符, const struct sockaddr *地址, socklen_t 地址长度);
ssize_t sendto(int 文件描述符, const void *数据, size_t 字节个数, int 设置,
               const struct sockaddr *地址, socklen_t 地址长度);
ssize_t recvfrom(int 文件描述符, void *数据, size_t 字节个数, int 设置,
                 struct sockaddr *地址, socklen_t *地址长度);
int getsockname(int 文件描述符, struct sockaddr *地址, socklen_t *地址长度);
int setsockopt(int 文件描述符, int 层值, int 设置名称, const void *值, socklen_t 值长度);
#endif
