#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define stofna_endastöð socket
#define BIND_slóð bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define breyta_Net_Stillingar setsockopt
#define þátta_Net_slóð inet_pton
#define snið_Net_slóð inet_ntop
#define 망차례짧은수 htons
#define Net_heiltala htonl
#define 장치차례짧은수 ntohs
#define tæki_röð_heiltala ntohl
#endif
