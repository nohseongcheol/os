#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_ADDRESS bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define newid_Rhwydwaith_Gosodiadau setsockopt
#define dosrannu_Rhwydwaith_ADDRESS inet_pton
#define fformat_Rhwydwaith_ADDRESS inet_ntop
#define 망차례짧은수 htons
#define Rhwydwaith_cyfanrif htonl
#define 장치차례짧은수 ntohs
#define dyfais_trefn_cyfanrif ntohl
#endif
