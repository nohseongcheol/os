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
int bind(int дескриптор_файла, const struct sockaddr *address, socklen_t address_len);
int connect(int дескриптор_файла, const struct sockaddr *address, socklen_t address_len);
int listen(int дескриптор_файла, int backlog);
int accept(int дескриптор_файла, struct sockaddr *address, socklen_t *address_len);
int getsockname(int дескриптор_файла, struct sockaddr *address, socklen_t *address_len);
int getpeername(int дескриптор_файла, struct sockaddr *address, socklen_t *address_len);
ssize_t send(int дескриптор_файла, const void *буфер_передавання_2, size_t довжина, int flags);
ssize_t recv(int дескриптор_файла, void *буфер_передавання_2, size_t довжина, int flags);
ssize_t sendto(int дескриптор_файла, const void *message, size_t довжина, int flags,
               const struct sockaddr *dest_addr, socklen_t dest_len);
ssize_t recvfrom(int дескриптор_файла, void *буфер_передавання_2, size_t довжина, int flags,
                 struct sockaddr *address, socklen_t *address_len);
int shutdown(int дескриптор_файла, int how);
int setsockopt(int дескриптор_файла, int level, int option_name,
               const void *option_value, socklen_t option_len);
#ifdef __cplusplus
}
#endif

#endif
