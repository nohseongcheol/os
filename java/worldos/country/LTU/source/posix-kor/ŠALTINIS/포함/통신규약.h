#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define kurti_dalyvis socket
#define BIND_ADDRESS bind
#define siųsti_paketų_kelio_schema_duomenys sendto
#define gauti_paketų_kelio_schema_duomenys recvfrom
#define 통신주소읽기 getsockname
#define keisti_tinklas_Parametrai setsockopt
#define analizuoti_sintaksę_tinklo_identifikatorius inet_pton
#define formatas_tinklo_identifikatorius inet_ntop
#define 망차례짧은수 htons
#define tinklas_sveikasis_skaičius htonl
#define 장치차례짧은수 ntohs
#define įrenginys_tvarka_sveikasis_skaičius ntohl
#endif
