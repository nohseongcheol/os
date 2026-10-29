#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define avama_osaleja socket
#define BIND_ADDRESS bind
#define saatma_datagramm_andmed sendto
#define saama_datagramm_andmed recvfrom
#define 통신주소읽기 getsockname
#define muutma_võrk_Sätted setsockopt
#define sõeluma_võrgu_ID inet_pton
#define vorming_võrgu_ID inet_ntop
#define 망차례짧은수 htons
#define võrk_täisarv htonl
#define 장치차례짧은수 ntohs
#define seade_tellimus_täisarv ntohl
#endif
