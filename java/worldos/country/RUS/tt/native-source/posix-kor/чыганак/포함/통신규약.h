#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_адрес bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define үзгәртү_Челтәр_Параметрлар setsockopt
#define бүлү_Челтәр_адрес inet_pton
#define формат_Челтәр_адрес inet_ntop
#define 망차례짧은수 htons
#define Челтәр_бөтен_сан htonl
#define 장치차례짧은수 ntohs
#define мобиль_тәртипкә_салу_бөтен_сан ntohl
#endif
