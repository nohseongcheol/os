#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define холбох_хаяг bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define өөрчлөх_Сүлжээ_Тохиргоо setsockopt
#define задлан_ялгал_хийх_Сүлжээ_хаяг inet_pton
#define формат_Сүлжээ_хаяг inet_ntop
#define 망차례짧은수 htons
#define Сүлжээ_бүхэл_тоо htonl
#define 장치차례짧은수 ntohs
#define гар_утас_дараалал_бүхэл_тоо ntohl
#endif
