#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Opprett_endepunkt socket
#define BIND_ADDRESS bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define endre_Nettverk_Innstillingar setsockopt
#define dele_opp_Nettverk_ADDRESS inet_pton
#define format_Nettverk_ADDRESS inet_ntop
#define 망차례짧은수 htons
#define Nettverk_heiltal htonl
#define 장치차례짧은수 ntohs
#define mobil_rekkjefølgje_heiltal ntohl
#endif
