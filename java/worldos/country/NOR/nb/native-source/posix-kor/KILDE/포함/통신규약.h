#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define åpne_deltaker socket
#define BIND_e_post bind
#define sende_datagram_data sendto
#define motta_datagram_data recvfrom
#define 통신주소읽기 getsockname
#define endre_nettverk_Innstillinger setsockopt
#define dele_opp_nettverks_ID inet_pton
#define format_nettverks_ID inet_ntop
#define 망차례짧은수 htons
#define nettverk_heltall htonl
#define 장치차례짧은수 ntohs
#define enhet_ordre_heltall ntohl
#endif
