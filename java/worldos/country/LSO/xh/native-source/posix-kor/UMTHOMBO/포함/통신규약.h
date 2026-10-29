#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BOPHELELA_idilesi bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define tshintsha_Inethiwekhi_Iisetingi setsockopt
#define ingcaciso_yegama_Inethiwekhi_idilesi inet_pton
#define fomatha_Inethiwekhi_idilesi inet_ntop
#define 망차례짧은수 htons
#define Inethiwekhi_inani_elipheleleyo htonl
#define 장치차례짧은수 ntohs
#define isixhobo_ulandelelwano_inani_elipheleleyo ntohl
#endif
