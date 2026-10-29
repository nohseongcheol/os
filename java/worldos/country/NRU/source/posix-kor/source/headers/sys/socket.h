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
int socket(int addressScheme, int networkKind, int contractNumber);
int bind(int fileDescriptor, const struct sockaddr *address, socklen_t addressLength);
ssize_t sendto(int fileDescriptor, const void *data, size_t byteCount, int settings,
               const struct sockaddr *address, socklen_t addressLength);
ssize_t recvfrom(int fileDescriptor, void *data, size_t byteCount, int settings,
                 struct sockaddr *address, socklen_t *addressLength);
int getsockname(int fileDescriptor, struct sockaddr *address, socklen_t *addressLength);
int setsockopt(int fileDescriptor, int layerValue, int settingsName, const void *value, socklen_t valueLength);
#endif
