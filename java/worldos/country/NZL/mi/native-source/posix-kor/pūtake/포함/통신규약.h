#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_ADDRESS bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define huri_whatunga_Ngā_Tautuhinga setsockopt
#define poroporo_whatunga_ADDRESS inet_pton
#define hōputu_whatunga_ADDRESS inet_ntop
#define 망차례짧은수 htons
#define whatunga_tau_tōpū htonl
#define 장치차례짧은수 ntohs
#define pūkoro_whakaraupapa_tau_tōpū ntohl
#endif
