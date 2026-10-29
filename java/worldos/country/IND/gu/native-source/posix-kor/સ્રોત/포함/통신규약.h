#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define બાઇંડ_કરો_સરનામું bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define પરિવર્તન_કરો_નેટવર્ક_સેટિંગ્સ setsockopt
#define પાર્સ_કરો_નેટવર્ક_સરનામું inet_pton
#define સ્વરૂપ_નેટવર્ક_સરનામું inet_ntop
#define 망차례짧은수 htons
#define નેટવર્ક_પૂર્ણાંક htonl
#define 장치차례짧은수 ntohs
#define ડિવાઇસ_ક્રમ_પૂર્ણાંક ntohl
#endif
