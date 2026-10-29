#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define crear_extremo socket
#define ligar_ENDEREZO bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define modificar_Rede_Configuración setsockopt
#define analizar_Rede_ENDEREZO inet_pton
#define formato_Rede_ENDEREZO inet_ntop
#define 망차례짧은수 htons
#define Rede_número_enteiro htonl
#define 장치차례짧은수 ntohs
#define dispositivo_orde_número_enteiro ntohl
#endif
