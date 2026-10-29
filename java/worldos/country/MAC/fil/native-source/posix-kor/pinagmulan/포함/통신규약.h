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
#define baguhin_Network_Mga_Setting setsockopt
#define mag_parse_Network_email inet_pton
#define format_Network_email inet_ntop
#define 망차례짧은수 htons
#define Network_integer_buong_numero htonl
#define 장치차례짧은수 ntohs
#define device_pagkakasunud_sunod_integer_buong_numero ntohl
#endif
