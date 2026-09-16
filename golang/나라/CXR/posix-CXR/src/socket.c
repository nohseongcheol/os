/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <network_conversion/byte_order.h>
#include <system/syscall.h>
#include <system/socket.h>

enum { socket_call_number = 102 };
enum {
    SC_socket = 1, SC_bind = 2, SC_connect = 3, SC_listen = 4,
    SC_accept = 5, SC_getsockname = 6, SC_getpeername = 7,
    SC_send = 9, SC_recv = 10, SC_sendto = 11, SC_recvfrom = 12,
    SC_shutdown = 13, SC_setsockopt = 14
};

static long socket_call(long call, unsigned long *arguments)
{
    return __syscall_result(
        __syscall6(socket_call_number, call, (long)arguments, 0, 0, 0, 0));
}

unsigned_16_bit_integer htons(unsigned_16_bit_integer value) { return (unsigned_16_bit_integer)((value << 8) | (value >> 8)); }
unsigned_16_bit_integer ntohs(unsigned_16_bit_integer value) { return htons(value); }
unsigned_32_bit_integer htonl(unsigned_32_bit_integer value)
{
    return ((value & 0x000000ffU) << 24) | ((value & 0x0000ff00U) << 8) |
           ((value & 0x00ff0000U) >> 8) | ((value & 0xff000000U) >> 24);
}
unsigned_32_bit_integer ntohl(unsigned_32_bit_integer value) { return htonl(value); }

int socket(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_socket, a);
}

int bind(int file_descriptor, const struct endpoint_address *address, address_length_type length)
{
    unsigned long a[3] = {(unsigned long)file_descriptor, (unsigned long)address, length};
    return (int)socket_call(SC_bind, a);
}

int connect(int file_descriptor, const struct endpoint_address *address, address_length_type length)
{
    unsigned long a[3] = {(unsigned long)file_descriptor, (unsigned long)address, length};
    return (int)socket_call(SC_connect, a);
}

int listen(int file_descriptor, int backlog)
{
    unsigned long a[2] = {(unsigned long)file_descriptor, (unsigned long)backlog};
    return (int)socket_call(SC_listen, a);
}

int accept(int file_descriptor, struct endpoint_address *address, address_length_type *length)
{
    unsigned long a[3] = {(unsigned long)file_descriptor, (unsigned long)address, (unsigned long)length};
    return (int)socket_call(SC_accept, a);
}

int getsockname(int file_descriptor, struct endpoint_address *address, address_length_type *length)
{
    unsigned long a[3] = {(unsigned long)file_descriptor, (unsigned long)address, (unsigned long)length};
    return (int)socket_call(SC_getsockname, a);
}

int getpeername(int file_descriptor, struct endpoint_address *address, address_length_type *length)
{
    unsigned long a[3] = {(unsigned long)file_descriptor, (unsigned long)address, (unsigned long)length};
    return (int)socket_call(SC_getpeername, a);
}

signed_size_type send(int file_descriptor, const void *transfer_buffer_2, object_size_type length, int flags)
{
    unsigned long a[4] = {(unsigned long)file_descriptor, (unsigned long)transfer_buffer_2, length, (unsigned long)flags};
    return (signed_size_type)socket_call(SC_send, a);
}

signed_size_type recv(int file_descriptor, void *transfer_buffer_2, object_size_type length, int flags)
{
    unsigned long a[4] = {(unsigned long)file_descriptor, (unsigned long)transfer_buffer_2, length, (unsigned long)flags};
    return (signed_size_type)socket_call(SC_recv, a);
}

signed_size_type sendto(int file_descriptor, const void *transfer_buffer_2, object_size_type length, int flags,
               const struct endpoint_address *address, address_length_type address_length)
{
    unsigned long a[6] = {(unsigned long)file_descriptor, (unsigned long)transfer_buffer_2, length,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (signed_size_type)socket_call(SC_sendto, a);
}

signed_size_type recvfrom(int file_descriptor, void *transfer_buffer_2, object_size_type length, int flags,
                 struct endpoint_address *address, address_length_type *address_length)
{
    unsigned long a[6] = {(unsigned long)file_descriptor, (unsigned long)transfer_buffer_2, length,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (signed_size_type)socket_call(SC_recvfrom, a);
}

int shutdown(int file_descriptor, int how)
{
    unsigned long a[2] = {(unsigned long)file_descriptor, (unsigned long)how};
    return (int)socket_call(SC_shutdown, a);
}

int setsockopt(int file_descriptor, int level, int option_name,
               const void *option_value, address_length_type option_len)
{
    unsigned long a[5] = {(unsigned long)file_descriptor, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_setsockopt, a);
}
