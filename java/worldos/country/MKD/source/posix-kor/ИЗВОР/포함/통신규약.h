#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define БИНД_адреса bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define измени_Мрежа_Параметри setsockopt
#define разложи_Мрежа_адреса inet_pton
#define формат_Мрежа_адреса inet_ntop
#define 망차례짧은수 htons
#define Мрежа_цел_број htonl
#define 장치차례짧은수 ntohs
#define уред_редослед_цел_број ntohl
#endif
