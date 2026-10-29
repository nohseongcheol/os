#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Create_účastník socket
#define BIND_adresa bind
#define odoslať_datagram_údaje sendto
#define dostať_datagram_údaje recvfrom
#define 통신주소읽기 getsockname
#define zmeniť_sieť_Nastavenia setsockopt
#define analyzovať_sieťová_identifikácia inet_pton
#define formát_sieťová_identifikácia inet_ntop
#define 망차례짧은수 htons
#define sieť_celé_číslo htonl
#define 장치차례짧은수 ntohs
#define telefón_poradie_celé_číslo ntohl
#endif
