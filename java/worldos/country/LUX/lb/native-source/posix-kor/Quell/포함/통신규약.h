#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BANNEN_Adress bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define änneren_Reseau_Astellungen setsockopt
#define analyséieren_Reseau_Adress inet_pton
#define Format_Reseau_Adress inet_ntop
#define 망차례짧은수 htons
#define Reseau_Ganzzuel htonl
#define 장치차례짧은수 ntohs
#define Mobil_Reiefolleg_Ganzzuel ntohl
#endif
