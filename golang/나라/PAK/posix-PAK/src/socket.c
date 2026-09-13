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

static long socket_call(long call, unsigned long *دلائل)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)دلائل, 0, 0, 0, 0));
}

uint16_t htons(uint16_t قدر) { return (uint16_t)((قدر << 8) | (قدر >> 8)); }
uint16_t ntohs(uint16_t قدر) { return htons(قدر); }
uint32_t htonl(uint32_t قدر)
{
    return ((قدر & 0x000000ffU) << 24) | ((قدر & 0x0000ff00U) << 8) |
           ((قدر & 0x00ff0000U) >> 8) | ((قدر & 0xff000000U) >> 24);
}
uint32_t ntohl(uint32_t قدر) { return htonl(قدر); }

int socket(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_socket, a);
}

int bind(int فائل_کا_وصف_کنندہ, const struct sockaddr *address, socklen_t لمبائی)
{
    unsigned long a[3] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)address, لمبائی};
    return (int)socket_call(SC_bind, a);
}

int connect(int فائل_کا_وصف_کنندہ, const struct sockaddr *address, socklen_t لمبائی)
{
    unsigned long a[3] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)address, لمبائی};
    return (int)socket_call(SC_connect, a);
}

int listen(int فائل_کا_وصف_کنندہ, int backlog)
{
    unsigned long a[2] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)backlog};
    return (int)socket_call(SC_listen, a);
}

int accept(int فائل_کا_وصف_کنندہ, struct sockaddr *address, socklen_t *لمبائی)
{
    unsigned long a[3] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)address, (unsigned long)لمبائی};
    return (int)socket_call(SC_accept, a);
}

int getsockname(int فائل_کا_وصف_کنندہ, struct sockaddr *address, socklen_t *لمبائی)
{
    unsigned long a[3] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)address, (unsigned long)لمبائی};
    return (int)socket_call(SC_getsockname, a);
}

int getpeername(int فائل_کا_وصف_کنندہ, struct sockaddr *address, socklen_t *لمبائی)
{
    unsigned long a[3] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)address, (unsigned long)لمبائی};
    return (int)socket_call(SC_getpeername, a);
}

ssize_t send(int فائل_کا_وصف_کنندہ, const void *منتقلی_کا_عارضی_ذخیرہ_2, size_t لمبائی, int flags)
{
    unsigned long a[4] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)منتقلی_کا_عارضی_ذخیرہ_2, لمبائی, (unsigned long)flags};
    return (ssize_t)socket_call(SC_send, a);
}

ssize_t recv(int فائل_کا_وصف_کنندہ, void *منتقلی_کا_عارضی_ذخیرہ_2, size_t لمبائی, int flags)
{
    unsigned long a[4] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)منتقلی_کا_عارضی_ذخیرہ_2, لمبائی, (unsigned long)flags};
    return (ssize_t)socket_call(SC_recv, a);
}

ssize_t sendto(int فائل_کا_وصف_کنندہ, const void *منتقلی_کا_عارضی_ذخیرہ_2, size_t لمبائی, int flags,
               const struct sockaddr *address, socklen_t address_length)
{
    unsigned long a[6] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)منتقلی_کا_عارضی_ذخیرہ_2, لمبائی,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_sendto, a);
}

ssize_t recvfrom(int فائل_کا_وصف_کنندہ, void *منتقلی_کا_عارضی_ذخیرہ_2, size_t لمبائی, int flags,
                 struct sockaddr *address, socklen_t *address_length)
{
    unsigned long a[6] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)منتقلی_کا_عارضی_ذخیرہ_2, لمبائی,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_recvfrom, a);
}

int shutdown(int فائل_کا_وصف_کنندہ, int how)
{
    unsigned long a[2] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)how};
    return (int)socket_call(SC_shutdown, a);
}

int setsockopt(int فائل_کا_وصف_کنندہ, int level, int option_name,
               const void *option_value, socklen_t option_len)
{
    unsigned long a[5] = {(unsigned long)فائل_کا_وصف_کنندہ, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_setsockopt, a);
}
