/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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

static long socket_call(long call, unsigned long *argomenti)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)argomenti, 0, 0, 0, 0));
}

uint16_t htons(uint16_t valore) { return (uint16_t)((valore << 8) | (valore >> 8)); }
uint16_t ntohs(uint16_t valore) { return htons(valore); }
uint32_t htonl(uint32_t valore)
{
    return ((valore & 0x000000ffU) << 24) | ((valore & 0x0000ff00U) << 8) |
           ((valore & 0x00ff0000U) >> 8) | ((valore & 0xff000000U) >> 24);
}
uint32_t ntohl(uint32_t valore) { return htonl(valore); }

int socket(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_socket, a);
}

int bind(int descrittore_del_file, const struct sockaddr *address, socklen_t lunghezza)
{
    unsigned long a[3] = {(unsigned long)descrittore_del_file, (unsigned long)address, lunghezza};
    return (int)socket_call(SC_bind, a);
}

int connect(int descrittore_del_file, const struct sockaddr *address, socklen_t lunghezza)
{
    unsigned long a[3] = {(unsigned long)descrittore_del_file, (unsigned long)address, lunghezza};
    return (int)socket_call(SC_connect, a);
}

int listen(int descrittore_del_file, int backlog)
{
    unsigned long a[2] = {(unsigned long)descrittore_del_file, (unsigned long)backlog};
    return (int)socket_call(SC_listen, a);
}

int accept(int descrittore_del_file, struct sockaddr *address, socklen_t *lunghezza)
{
    unsigned long a[3] = {(unsigned long)descrittore_del_file, (unsigned long)address, (unsigned long)lunghezza};
    return (int)socket_call(SC_accept, a);
}

int getsockname(int descrittore_del_file, struct sockaddr *address, socklen_t *lunghezza)
{
    unsigned long a[3] = {(unsigned long)descrittore_del_file, (unsigned long)address, (unsigned long)lunghezza};
    return (int)socket_call(SC_getsockname, a);
}

int getpeername(int descrittore_del_file, struct sockaddr *address, socklen_t *lunghezza)
{
    unsigned long a[3] = {(unsigned long)descrittore_del_file, (unsigned long)address, (unsigned long)lunghezza};
    return (int)socket_call(SC_getpeername, a);
}

ssize_t send(int descrittore_del_file, const void *memoria_intermedia_di_trasferimento_2, size_t lunghezza, int flags)
{
    unsigned long a[4] = {(unsigned long)descrittore_del_file, (unsigned long)memoria_intermedia_di_trasferimento_2, lunghezza, (unsigned long)flags};
    return (ssize_t)socket_call(SC_send, a);
}

ssize_t recv(int descrittore_del_file, void *memoria_intermedia_di_trasferimento_2, size_t lunghezza, int flags)
{
    unsigned long a[4] = {(unsigned long)descrittore_del_file, (unsigned long)memoria_intermedia_di_trasferimento_2, lunghezza, (unsigned long)flags};
    return (ssize_t)socket_call(SC_recv, a);
}

ssize_t sendto(int descrittore_del_file, const void *memoria_intermedia_di_trasferimento_2, size_t lunghezza, int flags,
               const struct sockaddr *address, socklen_t address_length)
{
    unsigned long a[6] = {(unsigned long)descrittore_del_file, (unsigned long)memoria_intermedia_di_trasferimento_2, lunghezza,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_sendto, a);
}

ssize_t recvfrom(int descrittore_del_file, void *memoria_intermedia_di_trasferimento_2, size_t lunghezza, int flags,
                 struct sockaddr *address, socklen_t *address_length)
{
    unsigned long a[6] = {(unsigned long)descrittore_del_file, (unsigned long)memoria_intermedia_di_trasferimento_2, lunghezza,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_recvfrom, a);
}

int shutdown(int descrittore_del_file, int how)
{
    unsigned long a[2] = {(unsigned long)descrittore_del_file, (unsigned long)how};
    return (int)socket_call(SC_shutdown, a);
}

int setsockopt(int descrittore_del_file, int level, int option_name,
               const void *option_value, socklen_t option_len)
{
    unsigned long a[5] = {(unsigned long)descrittore_del_file, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_setsockopt, a);
}
