#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Направи_крајња_тачка socket
#define повезати_адреса bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define промијенити_Мрежа_Поставке setsockopt
#define рашчланити_Мрежа_адреса inet_pton
#define формат_Мрежа_адреса inet_ntop
#define 망차례짧은수 htons
#define Мрежа_цијели_број htonl
#define 장치차례짧은수 ntohs
#define уређај_поредати_цијели_број ntohl
#endif
