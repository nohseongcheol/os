#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define կապել_հասցե bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define փոխել_Ցանց_Կարգավորումներ setsockopt
#define վերլուծել_Ցանց_հասցե inet_pton
#define ձեւաչափ_Ցանց_հասցե inet_ntop
#define 망차례짧은수 htons
#define Ցանց_ամբողջ_թիվ htonl
#define 장치차례짧은수 ntohs
#define սարք_կարգ_ամբողջ_թիվ ntohl
#endif
