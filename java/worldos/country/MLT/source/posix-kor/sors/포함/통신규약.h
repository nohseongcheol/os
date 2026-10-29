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
#define bidel_netwerk_Settings setsockopt
#define analizza_netwerk_ADDRESS inet_pton
#define format_netwerk_ADDRESS inet_ntop
#define 망차례짧은수 htons
#define netwerk_numru_sħiħ htonl
#define 장치차례짧은수 ntohs
#define mowbajl_ordni_numru_sħiħ ntohl
#endif
