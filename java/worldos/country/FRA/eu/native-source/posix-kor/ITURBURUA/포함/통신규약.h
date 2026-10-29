#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define sortu_amaiera_puntu socket
#define lotu_helbide bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define aldatu_sare_Ezarpenak setsockopt
#define analizatu_sare_helbide inet_pton
#define formatu_sare_helbide inet_ntop
#define 망차례짧은수 htons
#define sare_osoko_zenbaki htonl
#define 장치차례짧은수 ntohs
#define gailu_ordena_osoko_zenbaki ntohl
#endif
