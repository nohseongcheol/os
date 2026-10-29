#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define maken_eindpunt socket
#define BIND_ADRES bind
#define e_mailen_datagram_gegevens sendto
#define ontvangen_datagram_gegevens recvfrom
#define 통신주소읽기 getsockname
#define wijzigen_net_Instellingen setsockopt
#define parseren_netwerk_id inet_pton
#define opmaak_netwerk_id inet_ntop
#define 망차례짧은수 htons
#define net_geheel_getal htonl
#define 장치차례짧은수 ntohs
#define mobiel_order_geheel_getal ntohl
#endif
