#ifndef JKOROS_IN_H
#define JKOROS_IN_H
#include <stdint.h>
#include <sys/socket.h>
typedef uint16_t in_port_t;
typedef uint32_t in_addr_t;
struct in_addr { in_addr_t s_addr; };
struct sockaddr_in {
    sa_family_t sin_family;
    in_port_t sin_port;
    struct in_addr sin_addr;
    unsigned char sin_zero[8];
};
#define INADDR_ANY 0U
#define INADDR_LOOPBACK 0x7f000001U
#define IPPROTO_UDP 17
uint16_t htons(uint16_t balio);
uint16_t ntohs(uint16_t balio);
uint32_t htonl(uint32_t balio);
uint32_t ntohl(uint32_t balio);
#endif
