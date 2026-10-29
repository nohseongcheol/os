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
int socket(int 地址方案, int 網路種類, int 契約編號);
int bind(int 檔案描述符, const struct sockaddr *地址, socklen_t 地址長度);
ssize_t sendto(int 檔案描述符, const void *資料, size_t 位元組個數, int 設置,
               const struct sockaddr *地址, socklen_t 地址長度);
ssize_t recvfrom(int 檔案描述符, void *資料, size_t 位元組個數, int 設置,
                 struct sockaddr *地址, socklen_t *地址長度);
int getsockname(int 檔案描述符, struct sockaddr *地址, socklen_t *地址長度);
int setsockopt(int 檔案描述符, int 層值, int 設置名稱, const void *值, socklen_t 值長度);
#endif
