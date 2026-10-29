#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define készít_végpont socket
#define BIND_CÍM bind
#define küld_datagram_adat sendto
#define fogad_datagram_adat recvfrom
#define 통신주소읽기 getsockname
#define módosítás_hálózat_Gépház setsockopt
#define elemez_hálózati_azonosító inet_pton
#define formáz_hálózati_azonosító inet_ntop
#define 망차례짧은수 htons
#define hálózat_egész_szám htonl
#define 장치차례짧은수 ntohs
#define mobil_rendel_egész_szám ntohl
#endif
