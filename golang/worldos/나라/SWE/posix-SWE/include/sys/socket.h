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
int bind(int filbeskrivare, const struct sockaddr *address, socklen_t address_len);
int connect(int filbeskrivare, const struct sockaddr *address, socklen_t address_len);
int listen(int filbeskrivare, int backlog);
int accept(int filbeskrivare, struct sockaddr *address, socklen_t *address_len);
int getsockname(int filbeskrivare, struct sockaddr *address, socklen_t *address_len);
int getpeername(int filbeskrivare, struct sockaddr *address, socklen_t *address_len);
ssize_t send(int filbeskrivare, const void *överföringsbuffert_2, size_t längd, int flags);
ssize_t recv(int filbeskrivare, void *överföringsbuffert_2, size_t längd, int flags);
ssize_t sendto(int filbeskrivare, const void *message, size_t längd, int flags,
               const struct sockaddr *dest_addr, socklen_t dest_len);
ssize_t recvfrom(int filbeskrivare, void *överföringsbuffert_2, size_t längd, int flags,
                 struct sockaddr *address, socklen_t *address_len);
int shutdown(int filbeskrivare, int how);
int setsockopt(int filbeskrivare, int level, int option_name,
               const void *option_value, socklen_t option_len);
#ifdef __cplusplus
}
#endif

#endif
