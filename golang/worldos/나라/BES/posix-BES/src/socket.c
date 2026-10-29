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

static long socket_call(long call, unsigned long *argumenten)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)argumenten, 0, 0, 0, 0));
}

uint16_t htons(uint16_t waarde) { return (uint16_t)((waarde << 8) | (waarde >> 8)); }
uint16_t ntohs(uint16_t waarde) { return htons(waarde); }
uint32_t htonl(uint32_t waarde)
{
    return ((waarde & 0x000000ffU) << 24) | ((waarde & 0x0000ff00U) << 8) |
           ((waarde & 0x00ff0000U) >> 8) | ((waarde & 0xff000000U) >> 24);
}
uint32_t ntohl(uint32_t waarde) { return htonl(waarde); }

int socket(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_socket, a);
}

int bind(int bestandsdescriptor, const struct sockaddr *address, socklen_t lengte)
{
    unsigned long a[3] = {(unsigned long)bestandsdescriptor, (unsigned long)address, lengte};
    return (int)socket_call(SC_bind, a);
}

int connect(int bestandsdescriptor, const struct sockaddr *address, socklen_t lengte)
{
    unsigned long a[3] = {(unsigned long)bestandsdescriptor, (unsigned long)address, lengte};
    return (int)socket_call(SC_connect, a);
}

int listen(int bestandsdescriptor, int backlog)
{
    unsigned long a[2] = {(unsigned long)bestandsdescriptor, (unsigned long)backlog};
    return (int)socket_call(SC_listen, a);
}

int accept(int bestandsdescriptor, struct sockaddr *address, socklen_t *lengte)
{
    unsigned long a[3] = {(unsigned long)bestandsdescriptor, (unsigned long)address, (unsigned long)lengte};
    return (int)socket_call(SC_accept, a);
}

int getsockname(int bestandsdescriptor, struct sockaddr *address, socklen_t *lengte)
{
    unsigned long a[3] = {(unsigned long)bestandsdescriptor, (unsigned long)address, (unsigned long)lengte};
    return (int)socket_call(SC_getsockname, a);
}

int getpeername(int bestandsdescriptor, struct sockaddr *address, socklen_t *lengte)
{
    unsigned long a[3] = {(unsigned long)bestandsdescriptor, (unsigned long)address, (unsigned long)lengte};
    return (int)socket_call(SC_getpeername, a);
}

ssize_t send(int bestandsdescriptor, const void *overdrachtsbuffer_2, size_t lengte, int flags)
{
    unsigned long a[4] = {(unsigned long)bestandsdescriptor, (unsigned long)overdrachtsbuffer_2, lengte, (unsigned long)flags};
    return (ssize_t)socket_call(SC_send, a);
}

ssize_t recv(int bestandsdescriptor, void *overdrachtsbuffer_2, size_t lengte, int flags)
{
    unsigned long a[4] = {(unsigned long)bestandsdescriptor, (unsigned long)overdrachtsbuffer_2, lengte, (unsigned long)flags};
    return (ssize_t)socket_call(SC_recv, a);
}

ssize_t sendto(int bestandsdescriptor, const void *overdrachtsbuffer_2, size_t lengte, int flags,
               const struct sockaddr *address, socklen_t address_length)
{
    unsigned long a[6] = {(unsigned long)bestandsdescriptor, (unsigned long)overdrachtsbuffer_2, lengte,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_sendto, a);
}

ssize_t recvfrom(int bestandsdescriptor, void *overdrachtsbuffer_2, size_t lengte, int flags,
                 struct sockaddr *address, socklen_t *address_length)
{
    unsigned long a[6] = {(unsigned long)bestandsdescriptor, (unsigned long)overdrachtsbuffer_2, lengte,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_recvfrom, a);
}

int shutdown(int bestandsdescriptor, int how)
{
    unsigned long a[2] = {(unsigned long)bestandsdescriptor, (unsigned long)how};
    return (int)socket_call(SC_shutdown, a);
}

int setsockopt(int bestandsdescriptor, int level, int option_name,
               const void *option_value, socklen_t option_len)
{
    unsigned long a[5] = {(unsigned long)bestandsdescriptor, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_setsockopt, a);
}
