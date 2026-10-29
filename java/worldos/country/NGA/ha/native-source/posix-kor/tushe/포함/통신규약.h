#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_imel bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define Canza_Hanyar_sadarwa_Saituna setsockopt
#define Daddatse_Hanyar_sadarwa_imel inet_pton
#define zubi_Hanyar_sadarwa_imel inet_ntop
#define 망차례짧은수 htons
#define Hanyar_sadarwa_Lamba_mara htonl
#define 장치차례짧은수 ntohs
#define na_ura_Hanyar_jejjerawa_Lamba_mara ntohl
#endif
