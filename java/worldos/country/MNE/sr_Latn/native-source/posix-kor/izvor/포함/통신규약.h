#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Create_učesnik socket
#define povezati_adresa bind
#define poslati_datagram_podaci sendto
#define primiti_datagram_podaci recvfrom
#define 통신주소읽기 getsockname
#define promeniti_Mreža_Postavke setsockopt
#define raščlaniti_ID_mreže inet_pton
#define format_ID_mreže inet_ntop
#define 망차례짧은수 htons
#define Mreža_ceo_broj htonl
#define 장치차례짧은수 ntohs
#define uređaj_poručiti_ceo_broj ntohl
#endif
