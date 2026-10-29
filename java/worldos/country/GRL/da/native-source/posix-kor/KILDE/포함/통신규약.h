#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define åbne_slutpunkt socket
#define BIND_mail bind
#define maile_datagram_data sendto
#define modtage_datagram_data recvfrom
#define 통신주소읽기 getsockname
#define ændre_netværk_Indstillinger setsockopt
#define opdele_tekst_netværks_id inet_pton
#define format_netværks_id inet_ntop
#define 망차례짧은수 htons
#define netværk_heltal htonl
#define 장치차례짧은수 ntohs
#define enhed_ordre_heltal ntohl
#endif
