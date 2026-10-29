#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define atvērt_dalībnieks socket
#define BIND_adrese bind
#define sūtīt_datogramma_dati sendto
#define saņemt_datogramma_dati recvfrom
#define 통신주소읽기 getsockname
#define mainīt_tīkls_Iestatījumi setsockopt
#define parsēt_tīkla_ID inet_pton
#define formāts_tīkla_ID inet_ntop
#define 망차례짧은수 htons
#define tīkls_vesels_skaitlis htonl
#define 장치차례짧은수 ntohs
#define ierīce_secība_vesels_skaitlis ntohl
#endif
