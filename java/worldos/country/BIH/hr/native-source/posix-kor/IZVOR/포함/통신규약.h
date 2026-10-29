#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Create_sudionik socket
#define BIND_adresa bind
#define slati_datogram_podaci sendto
#define primiti_datogram_podaci recvfrom
#define 통신주소읽기 getsockname
#define promijeniti_mreža_Postavke setsockopt
#define rastavljati_mrežni_ID inet_pton
#define oblik_mrežni_ID inet_ntop
#define 망차례짧은수 htons
#define mreža_cijeli_broj htonl
#define 장치차례짧은수 ntohs
#define uređaj_narudžba_cijeli_broj ntohl
#endif
