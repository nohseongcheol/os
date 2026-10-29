#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Crea_endpoint socket
#define BIND_e_mail bind
#define inviare_datagramma_dati sendto
#define ricevere_datagramma_dati recvfrom
#define 통신주소읽기 getsockname
#define cambiare_rete_Impostazioni setsockopt
#define analizzare_ID_rete inet_pton
#define formato_ID_rete inet_ntop
#define 망차례짧은수 htons
#define rete_intero htonl
#define 장치차례짧은수 ntohs
#define cellulare_ordine_intero ntohl
#endif
