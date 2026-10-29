#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Ustvari_končna_točka socket
#define BIND_naslov bind
#define poslati_datagram_podatki sendto
#define sprejeti_sprejemati_prejeti_prejemati_datagram_podatki recvfrom
#define 통신주소읽기 getsockname
#define spremeniti_mreža_Nastavitve setsockopt
#define razčlenjevati_omrežni_identifikator inet_pton
#define oblika_omrežni_identifikator inet_ntop
#define 망차례짧은수 htons
#define mreža_celo_število htonl
#define 장치차례짧은수 ntohs
#define naprava_naročilo_celo_število ntohl
#endif
