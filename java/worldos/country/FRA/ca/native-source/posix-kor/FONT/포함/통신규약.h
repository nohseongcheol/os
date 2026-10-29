#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Crear_extrem socket
#define enllaçar_ADREÇA bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define canviar_xarxa_Configuració setsockopt
#define analitzar_xarxa_ADREÇA inet_pton
#define format_xarxa_ADREÇA inet_ntop
#define 망차례짧은수 htons
#define 망차례정수 htonl
#define 장치차례짧은수 ntohs
#define 장치차례정수 ntohl
#endif
