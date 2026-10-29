#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define прывязаць_адрас bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define змяніць_Сетка_Налады setsockopt
#define 망주소해석하기 inet_pton
#define фармат_Сетка_адрас inet_ntop
#define 망차례짧은수 htons
#define Сетка_цэлы_лік htonl
#define 장치차례짧은수 ntohs
#define прылада_парадак_цэлы_лік ntohl
#endif
