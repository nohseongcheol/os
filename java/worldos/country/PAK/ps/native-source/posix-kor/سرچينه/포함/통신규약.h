#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define اړه_لري_پته bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define 통신설정바꾸기 setsockopt
#define تجزیه_جال_پته inet_pton
#define بڼه_جال_پته inet_ntop
#define 망차례짧은수 htons
#define جال_صحيح_عدد htonl
#define 장치차례짧은수 ntohs
#define وزله_اڼن_اوډون_صحيح_عدد ntohl
#endif
