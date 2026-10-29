#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_salgy bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define üýtget_Tor_Sazlamalar setsockopt
#define seljer_Tor_salgy inet_pton
#define format_Tor_salgy inet_ntop
#define 망차례짧은수 htons
#define Tor_bitin htonl
#define 장치차례짧은수 ntohs
#define enjam_tertip_bitin ntohl
#endif
