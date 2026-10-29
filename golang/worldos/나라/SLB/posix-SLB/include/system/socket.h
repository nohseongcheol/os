#ifndef _include_system_socket
#define _include_system_socket

#include <basic_definitions.h>
#include <system/data_types.h>

typedef unsigned short address_family_type;

struct endpoint_address {
    address_family_type endpoint_address_family;
    char address_payload[14];
};

#define unspecified_address_family 0
#define internetwork_address_family_code 2
#define internetwork_protocol_family internetwork_address_family_code

#define stream_endpoint 1
#define datagram_endpoint 2

#define stop_receiving 0
#define stop_sending 1
#define stop_both_directions 2

#ifdef __cplusplus
extern "C" {
#endif
int socket(int domain, int type, int protocol);
int bind(int file_descriptor, const struct endpoint_address *address, address_length_type address_len);
int connect(int file_descriptor, const struct endpoint_address *address, address_length_type address_len);
int listen(int file_descriptor, int backlog);
int accept(int file_descriptor, struct endpoint_address *address, address_length_type *address_len);
int getsockname(int file_descriptor, struct endpoint_address *address, address_length_type *address_len);
int getpeername(int file_descriptor, struct endpoint_address *address, address_length_type *address_len);
signed_size_type send(int file_descriptor, const void *transfer_buffer_2, object_size_type length, int flags);
signed_size_type recv(int file_descriptor, void *transfer_buffer_2, object_size_type length, int flags);
signed_size_type sendto(int file_descriptor, const void *message, object_size_type length, int flags,
               const struct endpoint_address *dest_addr, address_length_type dest_len);
signed_size_type recvfrom(int file_descriptor, void *transfer_buffer_2, object_size_type length, int flags,
                 struct endpoint_address *address, address_length_type *address_len);
int shutdown(int file_descriptor, int how);
int setsockopt(int file_descriptor, int level, int option_name,
               const void *option_value, address_length_type option_len);
#ifdef __cplusplus
}
#endif

#endif
