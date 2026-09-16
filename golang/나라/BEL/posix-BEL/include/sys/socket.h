/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_SYS_SOCKET_H
#define _LIBC_SYS_SOCKET_H

#include <stddef.h>
#include <sys/types.h>

typedef unsigned short sa_family_t;

struct sockaddr {
    sa_family_t sa_family;
    char sa_data[14];
};

#define AF_UNSPEC 0
#define AF_INET 2
#define PF_INET AF_INET

#define SOCK_STREAM 1
#define SOCK_DGRAM 2

#define SHUT_RD 0
#define SHUT_WR 1
#define SHUT_RDWR 2

#ifdef __cplusplus
extern "C" {
#endif
int socket(int domain, int type, int protocol);
int bind(int bestandsdescriptor, const struct sockaddr *address, socklen_t address_len);
int connect(int bestandsdescriptor, const struct sockaddr *address, socklen_t address_len);
int listen(int bestandsdescriptor, int backlog);
int accept(int bestandsdescriptor, struct sockaddr *address, socklen_t *address_len);
int getsockname(int bestandsdescriptor, struct sockaddr *address, socklen_t *address_len);
int getpeername(int bestandsdescriptor, struct sockaddr *address, socklen_t *address_len);
ssize_t send(int bestandsdescriptor, const void *overdrachtsbuffer_2, size_t lengte, int flags);
ssize_t recv(int bestandsdescriptor, void *overdrachtsbuffer_2, size_t lengte, int flags);
ssize_t sendto(int bestandsdescriptor, const void *message, size_t lengte, int flags,
               const struct sockaddr *dest_addr, socklen_t dest_len);
ssize_t recvfrom(int bestandsdescriptor, void *overdrachtsbuffer_2, size_t lengte, int flags,
                 struct sockaddr *address, socklen_t *address_len);
int shutdown(int bestandsdescriptor, int how);
int setsockopt(int bestandsdescriptor, int level, int option_name,
               const void *option_value, socklen_t option_len);
#ifdef __cplusplus
}
#endif

#endif
