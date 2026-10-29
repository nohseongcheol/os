#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Twórca_uczestnik socket
#define BIND_ADRES bind
#define wysłać_datagram_dane sendto
#define odbierać_datagram_dane recvfrom
#define 통신주소읽기 getsockname
#define zmienić_sieć_Ustawienia setsockopt
#define analizować_identyfikator_sieciowy inet_pton
#define format_identyfikator_sieciowy inet_ntop
#define 망차례짧은수 htons
#define sieć_liczba_całkowita htonl
#define 장치차례짧은수 ntohs
#define urządzenie_zamówić_liczba_całkowita ntohl
#endif
