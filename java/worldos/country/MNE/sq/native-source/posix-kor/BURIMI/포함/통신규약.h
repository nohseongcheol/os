#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_email bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define ndryshoj_rrjet_cilësimet setsockopt
#define analizoj_rrjet_email inet_pton
#define format_rrjet_email inet_ntop
#define 망차례짧은수 htons
#define rrjet_numër_i_plotë htonl
#define 장치차례짧은수 ntohs
#define pajisje_renditja_numër_i_plotë ntohl
#endif
