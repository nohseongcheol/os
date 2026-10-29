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
int bind(int নথি_নির্দেশক, const struct sockaddr *address, socklen_t address_len);
int connect(int নথি_নির্দেশক, const struct sockaddr *address, socklen_t address_len);
int listen(int নথি_নির্দেশক, int backlog);
int accept(int নথি_নির্দেশক, struct sockaddr *address, socklen_t *address_len);
int getsockname(int নথি_নির্দেশক, struct sockaddr *address, socklen_t *address_len);
int getpeername(int নথি_নির্দেশক, struct sockaddr *address, socklen_t *address_len);
ssize_t send(int নথি_নির্দেশক, const void *স্থানান্তরের_অস্থায়ী_ভান্ডার_2, size_t দৈর্ঘ্য, int flags);
ssize_t recv(int নথি_নির্দেশক, void *স্থানান্তরের_অস্থায়ী_ভান্ডার_2, size_t দৈর্ঘ্য, int flags);
ssize_t sendto(int নথি_নির্দেশক, const void *message, size_t দৈর্ঘ্য, int flags,
               const struct sockaddr *dest_addr, socklen_t dest_len);
ssize_t recvfrom(int নথি_নির্দেশক, void *স্থানান্তরের_অস্থায়ী_ভান্ডার_2, size_t দৈর্ঘ্য, int flags,
                 struct sockaddr *address, socklen_t *address_len);
int shutdown(int নথি_নির্দেশক, int how);
int setsockopt(int নথি_নির্দেশক, int level, int option_name,
               const void *option_value, socklen_t option_len);
#ifdef __cplusplus
}
#endif

#endif
