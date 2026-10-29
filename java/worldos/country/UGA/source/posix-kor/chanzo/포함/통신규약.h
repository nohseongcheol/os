#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define FUNGA_anwani bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define badilisha_Mtandao_Mipangilio setsockopt
#define changanua_Mtandao_anwani inet_pton
#define umbiza_Mtandao_anwani inet_ntop
#define 망차례짧은수 htons
#define Mtandao_namba_kamili htonl
#define 장치차례짧은수 ntohs
#define kifaa_mpangilio_namba_kamili ntohl
#endif
