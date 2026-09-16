/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _include_internetwork_address
#define _include_internetwork_address

#include <integer_types.h>
#include <system/socket.h>

typedef unsigned_32_bit_integer internetwork_address_value_type;
typedef unsigned_16_bit_integer transport_port_number_type;

struct internetwork_address {
    internetwork_address_value_type address_value;
};

struct internetwork_endpoint_address {
    address_family_type internetwork_address_family;
    transport_port_number_type transport_port_number;
    struct internetwork_address internetwork_address_field;
    unsigned char address_padding[8];
};

#define default_internetwork_protocol 0
#define user_datagram_protocol 17
#define any_local_address ((internetwork_address_value_type)0x00000000U)
#define loopback_address ((internetwork_address_value_type)0x7f000001U)

#endif
