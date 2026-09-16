#include <arpa/inet.h>
#include <sys/syscall.h>
#include <sys/socket.h>

enum { SYS_socketcall = 102 };
enum {
    SC_socket = 1, SC_bind = 2, SC_connect = 3, SC_listen = 4,
    SC_accept = 5, SC_getsockname = 6, SC_getpeername = 7,
    SC_send = 9, SC_recv = 10, SC_sendto = 11, SC_recvfrom = 12,
    SC_shutdown = 13, SC_setsockopt = 14
};

static long socket_call(long call, unsigned long *argument_2)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)argument_2, 0, 0, 0, 0));
}

uint16_t htons(uint16_t värde) { return (uint16_t)((värde << 8) | (värde >> 8)); }
uint16_t ntohs(uint16_t värde) { return htons(värde); }
uint32_t htonl(uint32_t värde)
{
    return ((värde & 0x000000ffU) << 24) | ((värde & 0x0000ff00U) << 8) |
           ((värde & 0x00ff0000U) >> 8) | ((värde & 0xff000000U) >> 24);
}
uint32_t ntohl(uint32_t värde) { return htonl(värde); }

int socket(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_socket, a);
}

int bind(int filbeskrivare, const struct sockaddr *address, socklen_t längd)
{
    unsigned long a[3] = {(unsigned long)filbeskrivare, (unsigned long)address, längd};
    return (int)socket_call(SC_bind, a);
}

int connect(int filbeskrivare, const struct sockaddr *address, socklen_t längd)
{
    unsigned long a[3] = {(unsigned long)filbeskrivare, (unsigned long)address, längd};
    return (int)socket_call(SC_connect, a);
}

int listen(int filbeskrivare, int backlog)
{
    unsigned long a[2] = {(unsigned long)filbeskrivare, (unsigned long)backlog};
    return (int)socket_call(SC_listen, a);
}

int accept(int filbeskrivare, struct sockaddr *address, socklen_t *längd)
{
    unsigned long a[3] = {(unsigned long)filbeskrivare, (unsigned long)address, (unsigned long)längd};
    return (int)socket_call(SC_accept, a);
}

int getsockname(int filbeskrivare, struct sockaddr *address, socklen_t *längd)
{
    unsigned long a[3] = {(unsigned long)filbeskrivare, (unsigned long)address, (unsigned long)längd};
    return (int)socket_call(SC_getsockname, a);
}

int getpeername(int filbeskrivare, struct sockaddr *address, socklen_t *längd)
{
    unsigned long a[3] = {(unsigned long)filbeskrivare, (unsigned long)address, (unsigned long)längd};
    return (int)socket_call(SC_getpeername, a);
}

ssize_t send(int filbeskrivare, const void *överföringsbuffert_2, size_t längd, int flags)
{
    unsigned long a[4] = {(unsigned long)filbeskrivare, (unsigned long)överföringsbuffert_2, längd, (unsigned long)flags};
    return (ssize_t)socket_call(SC_send, a);
}

ssize_t recv(int filbeskrivare, void *överföringsbuffert_2, size_t längd, int flags)
{
    unsigned long a[4] = {(unsigned long)filbeskrivare, (unsigned long)överföringsbuffert_2, längd, (unsigned long)flags};
    return (ssize_t)socket_call(SC_recv, a);
}

ssize_t sendto(int filbeskrivare, const void *överföringsbuffert_2, size_t längd, int flags,
               const struct sockaddr *address, socklen_t address_length)
{
    unsigned long a[6] = {(unsigned long)filbeskrivare, (unsigned long)överföringsbuffert_2, längd,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_sendto, a);
}

ssize_t recvfrom(int filbeskrivare, void *överföringsbuffert_2, size_t längd, int flags,
                 struct sockaddr *address, socklen_t *address_length)
{
    unsigned long a[6] = {(unsigned long)filbeskrivare, (unsigned long)överföringsbuffert_2, längd,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_recvfrom, a);
}

int shutdown(int filbeskrivare, int how)
{
    unsigned long a[2] = {(unsigned long)filbeskrivare, (unsigned long)how};
    return (int)socket_call(SC_shutdown, a);
}

int setsockopt(int filbeskrivare, int level, int option_name,
               const void *option_value, socklen_t option_len)
{
    unsigned long a[5] = {(unsigned long)filbeskrivare, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_setsockopt, a);
}
