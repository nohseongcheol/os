#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define i_BIND_ikheli bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define guqula_iNethiwekhi_Amasethingi setsockopt
#define zawula_iNethiwekhi_ikheli inet_pton
#define misa_iNethiwekhi_ikheli inet_ntop
#define 망차례짧은수 htons
#define iNethiwekhi_inamba htonl
#define 장치차례짧은수 ntohs
#define idivayisi_ukuhleleka_inamba ntohl
#endif
