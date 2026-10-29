#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Create_završna_tačka socket
#define BIND_adresa bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define promijeniti_Mreža_Postavke setsockopt
#define raščlanjivati_Mreža_adresa inet_pton
#define format_Mreža_adresa inet_ntop
#define 망차례짧은수 htons
#define Mreža_cijeli_broj htonl
#define 장치차례짧은수 ntohs
#define uređaj_redoslijed_cijeli_broj ntohl
#endif
