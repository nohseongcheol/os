#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Create_účastník socket
#define vázat_ODKAZ bind
#define poslat_datagram_data sendto
#define dostat_datagram_data recvfrom
#define 통신주소읽기 getsockname
#define změnit_síť_Nastavení setsockopt
#define parsovat_ID_sítě inet_pton
#define formát_ID_sítě inet_ntop
#define 망차례짧은수 htons
#define síť_integer htonl
#define 장치차례짧은수 ntohs
#define mobilní_pořadí_integer ntohl
#endif
