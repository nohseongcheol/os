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
int bind(int deskryptor_pliku, const struct sockaddr *address, socklen_t address_len);
int connect(int deskryptor_pliku, const struct sockaddr *address, socklen_t address_len);
int listen(int deskryptor_pliku, int backlog);
int accept(int deskryptor_pliku, struct sockaddr *address, socklen_t *address_len);
int getsockname(int deskryptor_pliku, struct sockaddr *address, socklen_t *address_len);
int getpeername(int deskryptor_pliku, struct sockaddr *address, socklen_t *address_len);
ssize_t send(int deskryptor_pliku, const void *bufor_przesyłania_2, size_t długość, int flags);
ssize_t recv(int deskryptor_pliku, void *bufor_przesyłania_2, size_t długość, int flags);
ssize_t sendto(int deskryptor_pliku, const void *message, size_t długość, int flags,
               const struct sockaddr *dest_addr, socklen_t dest_len);
ssize_t recvfrom(int deskryptor_pliku, void *bufor_przesyłania_2, size_t długość, int flags,
                 struct sockaddr *address, socklen_t *address_len);
int shutdown(int deskryptor_pliku, int how);
int setsockopt(int deskryptor_pliku, int level, int option_name,
               const void *option_value, socklen_t option_len);
#ifdef __cplusplus
}
#endif

#endif
