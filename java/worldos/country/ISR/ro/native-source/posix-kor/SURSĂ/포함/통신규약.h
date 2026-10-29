#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define crea_participant socket
#define BIND_adresa bind
#define trimite_diagramă_informații_date sendto
#define primi_diagramă_informații_date recvfrom
#define 통신주소읽기 getsockname
#define schimba_rețea_Setări setsockopt
#define analiza_ID_rețea inet_pton
#define format_ID_rețea inet_ntop
#define 망차례짧은수 htons
#define rețea_întreg htonl
#define 장치차례짧은수 ntohs
#define mobil_ordine_întreg ntohl
#endif
