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

static long socket_call(long call, unsigned long *đối_số)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)đối_số, 0, 0, 0, 0));
}

uint16_t htons(uint16_t giá_trị) { return (uint16_t)((giá_trị << 8) | (giá_trị >> 8)); }
uint16_t ntohs(uint16_t giá_trị) { return htons(giá_trị); }
uint32_t htonl(uint32_t giá_trị)
{
    return ((giá_trị & 0x000000ffU) << 24) | ((giá_trị & 0x0000ff00U) << 8) |
           ((giá_trị & 0x00ff0000U) >> 8) | ((giá_trị & 0xff000000U) >> 24);
}
uint32_t ntohl(uint32_t giá_trị) { return htonl(giá_trị); }

int socket(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_socket, a);
}

int bind(int bộ_mô_tả_tệp, const struct sockaddr *address, socklen_t độ_dài)
{
    unsigned long a[3] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)address, độ_dài};
    return (int)socket_call(SC_bind, a);
}

int connect(int bộ_mô_tả_tệp, const struct sockaddr *address, socklen_t độ_dài)
{
    unsigned long a[3] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)address, độ_dài};
    return (int)socket_call(SC_connect, a);
}

int listen(int bộ_mô_tả_tệp, int backlog)
{
    unsigned long a[2] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)backlog};
    return (int)socket_call(SC_listen, a);
}

int accept(int bộ_mô_tả_tệp, struct sockaddr *address, socklen_t *độ_dài)
{
    unsigned long a[3] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)address, (unsigned long)độ_dài};
    return (int)socket_call(SC_accept, a);
}

int getsockname(int bộ_mô_tả_tệp, struct sockaddr *address, socklen_t *độ_dài)
{
    unsigned long a[3] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)address, (unsigned long)độ_dài};
    return (int)socket_call(SC_getsockname, a);
}

int getpeername(int bộ_mô_tả_tệp, struct sockaddr *address, socklen_t *độ_dài)
{
    unsigned long a[3] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)address, (unsigned long)độ_dài};
    return (int)socket_call(SC_getpeername, a);
}

ssize_t send(int bộ_mô_tả_tệp, const void *bộ_đệm_truyền_2, size_t độ_dài, int flags)
{
    unsigned long a[4] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)bộ_đệm_truyền_2, độ_dài, (unsigned long)flags};
    return (ssize_t)socket_call(SC_send, a);
}

ssize_t recv(int bộ_mô_tả_tệp, void *bộ_đệm_truyền_2, size_t độ_dài, int flags)
{
    unsigned long a[4] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)bộ_đệm_truyền_2, độ_dài, (unsigned long)flags};
    return (ssize_t)socket_call(SC_recv, a);
}

ssize_t sendto(int bộ_mô_tả_tệp, const void *bộ_đệm_truyền_2, size_t độ_dài, int flags,
               const struct sockaddr *address, socklen_t address_length)
{
    unsigned long a[6] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)bộ_đệm_truyền_2, độ_dài,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_sendto, a);
}

ssize_t recvfrom(int bộ_mô_tả_tệp, void *bộ_đệm_truyền_2, size_t độ_dài, int flags,
                 struct sockaddr *address, socklen_t *address_length)
{
    unsigned long a[6] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)bộ_đệm_truyền_2, độ_dài,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_recvfrom, a);
}

int shutdown(int bộ_mô_tả_tệp, int how)
{
    unsigned long a[2] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)how};
    return (int)socket_call(SC_shutdown, a);
}

int setsockopt(int bộ_mô_tả_tệp, int level, int option_name,
               const void *option_value, socklen_t option_len)
{
    unsigned long a[5] = {(unsigned long)bộ_mô_tả_tệp, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_setsockopt, a);
}
