#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define உருவாக்கு_முடிவுப்_புள்ளி socket
#define கட்டு_முகவரி bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define மாற்று_பிணையம்_அமைப்புகள் setsockopt
#define அலகிடு_பிணையம்_முகவரி inet_pton
#define வடிவமை_பிணையம்_முகவரி inet_ntop
#define 망차례짧은수 htons
#define பிணையம்_முழு_எண் htonl
#define 장치차례짧은수 ntohs
#define சாதனம்_வரிசை_முழு_எண் ntohl
#endif
