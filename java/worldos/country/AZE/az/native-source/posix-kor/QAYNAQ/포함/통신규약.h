#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_ünvan bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define dəyişdirmək_Şəbəkə_Parametrlər setsockopt
#define parselləmək_Şəbəkə_ünvan inet_pton
#define format_Şəbəkə_ünvan inet_ntop
#define 망차례짧은수 htons
#define Şəbəkə_tam_ədəd htonl
#define 장치차례짧은수 ntohs
#define cihaz_ardıcıllıq_tam_ədəd ntohl
#endif
