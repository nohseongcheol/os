#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_adres bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define verander_Netwerk_Instellings setsockopt
#define ontleed_Netwerk_adres inet_pton
#define formaat_Netwerk_adres inet_ntop
#define 망차례짧은수 htons
#define Netwerk_heelgetal htonl
#define 장치차례짧은수 ntohs
#define mobiel_volgorde_heelgetal ntohl
#endif
