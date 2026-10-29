#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Skapa_deltagare socket
#define BIND_ADRESS bind
#define skicka_datagram_data sendto
#define få_datagram_data recvfrom
#define läsa_socket_ADRESS getsockname
#define ändra_nätverk_Inställningar setsockopt
#define parsa_Nätverks_ID inet_pton
#define format_Nätverks_ID inet_ntop
#define 망차례짧은수 htons
#define nätverk_heltal htonl
#define 장치차례짧은수 ntohs
#define enhet_order_heltal ntohl
#endif
